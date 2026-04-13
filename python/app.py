import json
import logging
import os
import re
import shutil
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

import google.generativeai as genai
import speech_recognition as sr
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydub import AudioSegment
from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Interview, Room, User
from schemas import AuthResponse, AuthSigninIn, AuthSignupIn, InterviewOut, RoomCreateIn, RoomJoinIn, RoomOut, UserOut
from security import create_access_token, decode_access_token, get_password_hash, parse_bearer_token, verify_password


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
model = None


def get_gemini_model():
    global model
    if model is None:
        if not GEMINI_API_KEY:
            raise HTTPException(status_code=503, detail="GEMINI_API_KEY is not configured")
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
    return model


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    yield


ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def user_out(user: User) -> UserOut:
    return UserOut.model_validate(user)


def room_out(room: Room) -> RoomOut:
    return RoomOut.model_validate(room)


def interview_out(interview: Interview, room: Optional[Room] = None) -> InterviewOut:
    return InterviewOut(
        id=interview.id,
        room_id=interview.room_id,
        room_code=room.code if room else None,
        interviewer_id=interview.interviewer_id,
        candidate_id=interview.candidate_id,
        created_by_id=interview.created_by_id,
        audio_file=interview.audio_file,
        json_file=interview.json_file,
        full_transcript=interview.full_transcript,
        qa_pairs=interview.qa_pairs or [],
        evaluation_report=interview.evaluation_report or {},
        status=interview.status,
        created_at=interview.created_at,
        completed_at=interview.completed_at,
    )


def get_current_user(authorization: Optional[str], db: Session) -> User:
    try:
        token = parse_bearer_token(authorization)
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Missing subject")
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid or missing token") from exc

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def convert_to_wav(input_path, output_path):
    if input_path.endswith(".webm"):
        AudioSegment.from_file(input_path, format="webm").export(output_path, format="wav")
    else:
        AudioSegment.from_file(input_path).export(output_path, format="wav")


def transcribe_audio(wav_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except Exception:
            pass

    # Fallback: split long recordings into smaller chunks to improve recognition reliability.
    try:
        audio_segment = AudioSegment.from_wav(wav_path)
        chunk_ms = 30_000
        transcripts = []

        for start in range(0, len(audio_segment), chunk_ms):
            chunk = audio_segment[start : start + chunk_ms]
            if chunk.rms < 120:
                continue

            chunk_path = f"{wav_path}.chunk.{start}.wav"
            chunk.export(chunk_path, format="wav")

            try:
                with sr.AudioFile(chunk_path) as source:
                    chunk_audio = recognizer.record(source)
                text = recognizer.recognize_google(chunk_audio)
                if text:
                    transcripts.append(text)
            except Exception:
                pass
            finally:
                if os.path.exists(chunk_path):
                    os.remove(chunk_path)

        return " ".join(transcripts).strip()
    except Exception:
        return ""


def process_qa(raw_text):
    """Extract Q&A pairs from a raw interview transcript using Gemini."""
    try:
        qa_pairs = _extract_qa_with_llm(raw_text)
        if qa_pairs:
            full_text = " ".join(
                f"{p['question']} {p['answer']}" for p in qa_pairs
            ).strip()
            return full_text, qa_pairs
    except Exception as exc:
        logger.warning("LLM Q&A extraction failed: %s", exc)

    return raw_text, []


def _extract_qa_with_llm(raw_text: str) -> list[dict]:
    prompt = f"""You are an expert at analysing interview transcripts.

The following is a raw, unpunctuated transcript of a technical interview.
It contains one or more questions asked by the interviewer, each followed
by the candidate's answer.

Your task:
1. Identify every distinct question the interviewer asked.
2. For each question, extract the candidate's answer that follows it.
3. Clean up grammar and punctuation in both the question and the answer.
4. If a question has no answer (candidate was silent or was cut off),
   set the answer to an empty string.

Return ONLY a JSON array (no markdown, no explanation) in this exact format:
[
  {{"question": "...", "answer": "..."}},
  {{"question": "...", "answer": "..."}}
]

Transcript:
{raw_text}
"""
    response = get_gemini_model().generate_content(prompt)
    parsed = clean_json(response.text, fallback=[])
    if isinstance(parsed, list) and parsed:
        # Validate each entry has the required keys
        valid = []
        for item in parsed:
            if isinstance(item, dict) and "question" in item:
                valid.append({
                    "question": str(item["question"]).strip(),
                    "answer": str(item.get("answer", "")).strip(),
                })
        return valid
    return []


def _merge_transcripts_with_llm(interviewer_text: str, candidate_text: str) -> list[dict]:
    """Merge two separate audio transcripts (one per participant) into Q&A pairs."""
    prompt = f"""You are an expert at combining interview transcripts from a two-person video call.

Two participants recorded their audio separately during the same interview session.
Each person's microphone primarily captured their own voice, though there may be
some bleed-through of the other person's voice.

Transcript from the INTERVIEWER's microphone (primarily contains questions):
{interviewer_text}

Transcript from the CANDIDATE's microphone (primarily contains answers):
{candidate_text}

Your task:
1. Reconstruct the full interview conversation by matching the interviewer's
   questions with the candidate's corresponding answers.
2. Clean up grammar and punctuation in both questions and answers.
3. If a question has no matching answer, set the answer to an empty string.
4. If text appears that is neither a clear question nor answer, use your best
   judgment to classify it based on which microphone captured it.

Return ONLY a JSON array (no markdown, no explanation):
[
  {{"question": "...", "answer": "..."}},
  {{"question": "...", "answer": "..."}}
]
"""
    response = get_gemini_model().generate_content(prompt)
    parsed = clean_json(response.text, fallback=[])
    if isinstance(parsed, list) and parsed:
        valid = []
        for item in parsed:
            if isinstance(item, dict) and "question" in item:
                valid.append({
                    "question": str(item["question"]).strip(),
                    "answer": str(item.get("answer", "")).strip(),
                })
        return valid
    return []


def clean_json(text, fallback=None):
    if fallback is None:
        fallback = {"score": 0, "feedback": "Parsing error"}
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass
    try:
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass
    return fallback


def evaluate_single_pair(pair: dict, job_role: str, position: str) -> dict:
    """Evaluate a single Q&A pair using Gemini, considering job role and position level."""
    prompt = f"""You are a strict technical interview evaluator.

Context:
- Target Job Role: {job_role}
- Position Level: {position}

Interviewer's Question:
{pair["question"]}

Candidate's Answer:
{pair["answer"]}

Evaluate TWO things:

1. **Question Relevance** – Is this question relevant to the target job role ({job_role})?
   Rate as: "Highly Relevant", "Somewhat Relevant", or "Not Relevant".

2. **Question Difficulty** – Given the position level ({position}), is this question's difficulty appropriate?
   Rate as: "Too Easy", "Appropriate", or "Too Hard".

3. **Answer Score** – Score the candidate's answer from 0-100.
   - 90-100: Excellent, thorough and accurate
   - 70-89: Good, mostly correct with minor gaps
   - 50-69: Partial understanding, missing key details
   - 0-49: Poor or incorrect

4. **Feedback** – Give brief, specific technical feedback on the answer.

Return ONLY a JSON object (no markdown, no explanation):
{{
  "question_relevance": "Highly Relevant" | "Somewhat Relevant" | "Not Relevant",
  "difficulty_assessment": "Too Easy" | "Appropriate" | "Too Hard",
  "score": <int 0-100>,
  "feedback": "<brief feedback>"
}}
"""
    try:
        response = get_gemini_model().generate_content(prompt)
        data = clean_json(response.text)
    except Exception as exc:
        data = {"score": 0, "feedback": str(exc), "question_relevance": "Unknown", "difficulty_assessment": "Unknown"}

    return {
        "topic": job_role,
        "position": position,
        "question_relevance": data.get("question_relevance", "Unknown"),
        "difficulty_assessment": data.get("difficulty_assessment", "Unknown"),
        "score": data.get("score", 0),
        "feedback": data.get("feedback", ""),
    }


def persist_interview(db: Session, current_user: User, room: Room, audio_file: str, json_file: str, full_text: str, qa_pairs: list[dict], evaluation_report: dict) -> Interview:
    interview = Interview(
        room_id=room.id,
        interviewer_id=room.interviewer_id,
        candidate_id=room.candidate_id,
        created_by_id=current_user.id,
        audio_file=audio_file,
        json_file=json_file,
        full_transcript=full_text,
        qa_pairs=qa_pairs,
        evaluation_report=evaluation_report,
        status="completed",
        completed_at=datetime.utcnow(),
    )
    db.add(interview)
    room.status = "completed"
    room.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(interview)
    return interview


@app.post("/auth/signup", response_model=AuthResponse)
def signup(payload: AuthSignupIn, db: Session = Depends(get_db)):
    role = payload.role.strip().lower()
    if role not in {"interviewer", "candidate"}:
        raise HTTPException(status_code=400, detail="Role must be interviewer or candidate")

    existing_user = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email.lower(),
        password_hash=get_password_hash(payload.password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id, {"role": user.role, "email": user.email})
    return AuthResponse(access_token=token, user=user_out(user))


@app.post("/auth/signin", response_model=AuthResponse)
def signin(payload: AuthSigninIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user.id, {"role": user.role, "email": user.email})
    return AuthResponse(access_token=token, user=user_out(user))


@app.get("/auth/me", response_model=UserOut)
def me(authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db)):
    return user_out(get_current_user(authorization, db))


@app.post("/rooms/create", response_model=RoomOut)
def create_room(payload: RoomCreateIn, authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db)):
    user = get_current_user(authorization, db)
    if user.role != "interviewer":
        raise HTTPException(status_code=403, detail="Only interviewers can create rooms")

    room = Room(
        code=uuid.uuid4().hex[:8].upper(),
        name=payload.name or "Interview Room",
        job_role=payload.job_role,
        position=payload.position,
        interviewer_id=user.id,
        status="waiting",
        updated_at=datetime.utcnow(),
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return room_out(room)


@app.post("/rooms/join", response_model=RoomOut)
def join_room(payload: RoomJoinIn, authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db)):
    user = get_current_user(authorization, db)
    room = db.query(Room).filter(Room.code == payload.room_code.upper()).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.status == "closed":
        raise HTTPException(status_code=409, detail="Room is closed")

    if user.role == "candidate":
        if room.candidate_id and room.candidate_id != user.id:
            raise HTTPException(status_code=409, detail="Room already joined by another candidate")
        room.candidate_id = user.id
        room.status = "active"
    elif user.id == room.interviewer_id:
        room.status = "active"
    else:
        raise HTTPException(status_code=403, detail="Only the room interviewer can join with this account")

    room.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(room)
    return room_out(room)


@app.post("/rooms/{room_id}/close", response_model=RoomOut)
def close_room(room_id: str, authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db)):
    user = get_current_user(authorization, db)
    room = db.query(Room).filter(or_(Room.id == room_id, Room.code == room_id.upper())).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.interviewer_id != user.id:
        raise HTTPException(status_code=403, detail="Only the room interviewer can close this room")

    room.status = "closed"
    room.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(room)
    return room_out(room)


@app.get("/rooms/mine", response_model=list[RoomOut])
def my_rooms(authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db)):
    user = get_current_user(authorization, db)
    rooms = (
        db.query(Room)
        .filter(or_(Room.interviewer_id == user.id, Room.candidate_id == user.id))
        .order_by(desc(Room.created_at))
        .all()
    )
    return [room_out(room) for room in rooms]


@app.get("/interviews", response_model=list[InterviewOut])
def list_interviews(authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db)):
    user = get_current_user(authorization, db)
    interviews = (
        db.query(Interview)
        .join(Room, Room.id == Interview.room_id)
        .filter(
            Interview.status != "pending_merge",
            or_(
                Interview.interviewer_id == user.id,
                Interview.candidate_id == user.id,
                Room.interviewer_id == user.id,
                Room.candidate_id == user.id,
            )
        )
        .order_by(desc(Interview.created_at))
        .all()
    )
    room_ids = [item.room_id for item in interviews]
    rooms = db.query(Room).filter(Room.id.in_(room_ids)).all() if room_ids else []
    rooms_by_id = {room.id: room for room in rooms}
    return [interview_out(interview, rooms_by_id.get(interview.room_id)) for interview in interviews]


@app.get("/interviews/{interview_id}", response_model=InterviewOut)
def get_interview(interview_id: str, authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db)):
    user = get_current_user(authorization, db)
    interview = db.get(Interview, interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    if user.id not in {interview.interviewer_id, interview.candidate_id, interview.created_by_id}:
        raise HTTPException(status_code=403, detail="You do not have access to this interview")

    room = db.get(Room, interview.room_id)
    return interview_out(interview, room)


@app.get("/results/{interview_id}", response_model=InterviewOut)
def get_result(interview_id: str, authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db)):
    return get_interview(interview_id, authorization, db)


@app.post("/process-interview")
async def process_interview(
    file: UploadFile = File(...),
    room_id: str = Form(...),
    evaluate: str = Form(default="true"),
    authorization: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
):
    current_user = get_current_user(authorization, db)
    room = db.query(Room).filter(or_(Room.id == room_id, Room.code == room_id.upper())).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.status == "closed":
        raise HTTPException(status_code=409, detail="Room is closed")

    if current_user.id not in {room.interviewer_id, room.candidate_id}:
        if current_user.role == "candidate" and room.candidate_id is None:
            room.candidate_id = current_user.id
            room.status = "active"
            room.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(room)
        else:
            raise HTTPException(status_code=403, detail="You are not a participant in this room")

    uid = str(uuid.uuid4())
    temp_in = f"temp_{uid}"
    temp_wav = f"{temp_in}.wav"
    audio_dir = os.getenv("AUDIO_DIR", "./audio")
    os.makedirs(audio_dir, exist_ok=True)

    try:
        with open(temp_in, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        convert_to_wav(temp_in, temp_wav)
        raw_text = transcribe_audio(temp_wav)

        # Save audio to persistent storage
        audio_file_name = f"{os.path.splitext(os.path.basename(file.filename))[0]}-{uid}{os.path.splitext(file.filename)[1]}"
        audio_path = os.path.join(audio_dir, audio_file_name)
        with open(temp_in, "rb") as source, open(audio_path, "wb") as target:
            shutil.copyfileobj(source, target)

        # Check if there is already a pending submission for this room
        pending = db.query(Interview).filter(
            Interview.room_id == room.id,
            Interview.status == "pending_merge",
        ).first()

        if not pending:
            # ── FIRST UPLOAD: save transcript and wait for the other participant ──
            interview = Interview(
                room_id=room.id,
                interviewer_id=room.interviewer_id,
                candidate_id=room.candidate_id,
                created_by_id=current_user.id,
                audio_file=audio_path,
                full_transcript=raw_text or "",
                status="pending_merge",
            )
            db.add(interview)
            db.commit()
            db.refresh(interview)

            logger.info(
                "First submission for room %s by %s (%s). Waiting for second participant.",
                room.code, current_user.email, current_user.role,
            )

            return {
                "status": "pending_merge",
                "interview_id": interview.id,
                "room_id": room.id,
            }

        else:
            # ── SECOND UPLOAD: merge both transcripts and evaluate ──
            first_text = pending.full_transcript or ""
            second_text = raw_text or ""

            # Determine which transcript is the interviewer's and which is the candidate's
            if pending.created_by_id == room.interviewer_id:
                interviewer_text, candidate_text = first_text, second_text
            else:
                interviewer_text, candidate_text = second_text, first_text

            should_evaluate = evaluate.lower() != "false"

            if should_evaluate:
                logger.info(
                    "Second submission for room %s. Merging transcripts (interviewer: %d chars, candidate: %d chars).",
                    room.code, len(interviewer_text), len(candidate_text),
                )

                # Merge transcripts into Q&A pairs using LLM
                if interviewer_text and candidate_text:
                    qa_pairs = _merge_transcripts_with_llm(interviewer_text, candidate_text)
                    full_text = " ".join(
                        f"{p['question']} {p['answer']}" for p in qa_pairs
                    ).strip()
                elif interviewer_text or candidate_text:
                    # Only one side has audio — fall back to single-transcript extraction
                    full_text, qa_pairs = process_qa(interviewer_text or candidate_text)
                else:
                    full_text = ""
                    qa_pairs = []

                # Evaluate the merged Q&A pairs
                if qa_pairs:
                    results = []
                    total = 0
                    for pair in qa_pairs:
                        result = evaluate_single_pair(pair, room.job_role, room.position)
                        results.append(
                            {
                                "question": pair["question"],
                                "candidate_answer": pair["answer"],
                                **result,
                            }
                        )
                        total += result["score"]
                        time.sleep(1)

                    average_score = total / len(results) if results else 0
                    evaluation_report = {"total_score": average_score, "results": results}
                    process_status = "success"
                else:
                    evaluation_report = {
                        "total_score": 0,
                        "results": [],
                        "note": "Unable to extract Q&A pairs from the recordings.",
                    }
                    process_status = "partial"
            else:
                logger.info(
                    "Second submission for room %s. Evaluation skipped by interviewer.",
                    room.code,
                )
                full_text = f"{first_text} {second_text}".strip()
                qa_pairs = []
                evaluation_report = {
                    "total_score": 0,
                    "results": [],
                    "note": "Evaluation was skipped by the interviewer.",
                }
                process_status = "skipped"

            # Write merged result JSON
            json_file_name = f"{os.path.splitext(os.path.basename(file.filename))[0]}-{uid}.json"
            json_file_path = os.path.join(audio_dir, json_file_name)

            with open(json_file_path, "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "audioFile": audio_file_name,
                        "roomId": room.id,
                        "timestamp": datetime.utcnow().isoformat(),
                        "status": process_status,
                        "interviewer_transcript": interviewer_text,
                        "candidate_transcript": candidate_text,
                        "full_transcript": full_text,
                        "qa_pairs": qa_pairs,
                        "evaluation_report": evaluation_report,
                    },
                    handle,
                    indent=2,
                )

            # Update the pending interview record with merged results
            pending.full_transcript = full_text
            pending.qa_pairs = qa_pairs
            pending.evaluation_report = evaluation_report
            pending.json_file = json_file_path
            pending.status = "completed"
            pending.completed_at = datetime.utcnow()
            pending.candidate_id = room.candidate_id

            room.status = "completed"
            room.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(pending)

            return {
                "status": process_status,
                "interview_id": pending.id,
                "room_id": room.id,
                "full_transcript": full_text,
                "qa_pairs": qa_pairs,
                "evaluation_report": evaluation_report,
            }

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Interview processing failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        if os.path.exists(temp_in):
            os.remove(temp_in)
        if os.path.exists(temp_wav):
            os.remove(temp_wav)