# Fair View – AI-Powered Interview Platform

Fair View is a role-based video interview platform built with **React**, **WebRTC**, **Node.js**, and **FastAPI**. Interviewers create rooms, candidates join with a shared code, and the platform records, transcribes, and evaluates interviews using **Google Gemini**.

## Features

- **Role-based auth** — sign up as interviewer or candidate (JWT)
- **Room management** — create rooms with job role & seniority level, share a room code
- **WebRTC video calls** — peer-to-peer via ScaleDrone signaling
- **Dual audio recording** — each participant records independently
- **AI transcript merging** — Gemini combines both recordings into Q&A pairs
- **AI evaluation** — each answer is scored for relevance, difficulty, and quality
- **Interviewer call control** — only the interviewer can end the call and choose whether to evaluate
- **Persistent results** — scores, transcripts, and feedback are stored in SQLite

## Architecture

```
Browser (React 19)         localhost:3000
   ├── WebRTC via ScaleDrone
   └── Audio upload ──►  Node audio bridge   localhost:3001
                              └──►  FastAPI backend     localhost:8001
                                       ├── Google Gemini (transcription + eval)
                                       └── SQLite (users, rooms, interviews)
```

## Prerequisites

- **Node.js** v16+
- **Python** 3.10+
- **FFmpeg** — required by pydub for audio conversion
- A **ScaleDrone** account (free tier works) — [scaledrone.com](https://www.scaledrone.com/)
- A **Google Gemini** API key — [ai.google.dev](https://ai.google.dev/)

## Quick Start

### 1. Clone & configure environment variables

```bash
# Python backend
cp python/.env.example python/.env
# Edit python/.env and fill in GEMINI_API_KEY and JWT_SECRET_KEY

# React frontend
cp frontend-video/.env.example frontend-video/.env
# Edit frontend-video/.env and fill in REACT_APP_SCALEDRONE_ID

# Node audio bridge (optional — defaults work for local dev)
cp frontend-video/server/.env.example frontend-video/server/.env
```

### 2. Install dependencies

```bash
# Python
cd python
pip install -r requirements.txt

# React frontend
cd ../frontend-video
npm install

# Node audio bridge
cd server
npm install
```

### 3. Initialise the database

```bash
cd ../../python
python init_db.py
```

### 4. Start all three services

```bash
# Terminal 1 — Python API (port 8001)
cd python
uvicorn app:app --host 127.0.0.1 --port 8001

# Terminal 2 — Node audio bridge (port 3001)
cd frontend-video/server
npm start

# Terminal 3 — React dev server (port 3000)
cd frontend-video
npm start
```

## Environment Variables

### Python (`python/.env`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | **Yes** | — | Google Gemini API key |
| `JWT_SECRET_KEY` | **Yes** | `dev-secret-change-me` | Secret for signing JWT tokens |
| `DATABASE_URL` | No | `sqlite:///./fair_view.db` | SQLAlchemy database URL |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `720` | JWT token lifetime |
| `ALLOWED_ORIGINS` | No | `*` | Comma-separated CORS origins |
| `AUDIO_DIR` | No | `./audio` | Directory for audio/JSON files |

### React (`frontend-video/.env`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `REACT_APP_SCALEDRONE_ID` | **Yes** | — | ScaleDrone channel ID for WebRTC signaling |
| `REACT_APP_API_URL` | No | `http://127.0.0.1:8001` | Python API base URL |
| `REACT_APP_UPLOAD_URL` | No | `http://localhost:3001/save-audio` | Node audio bridge URL |

### Node bridge (`frontend-video/server/.env`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `PORT` | No | `3001` | Server port |
| `PYTHON_API_URL` | No | `http://127.0.0.1:8001/process-interview` | Python API endpoint |

## Usage

1. **Sign up** — create an account as interviewer or candidate.
2. **Create a room** (interviewer) — enter a job role and position level, then share the room code.
3. **Join the room** (candidate) — enter the room code from the dashboard.
4. **Conduct the interview** — video call runs peer-to-peer, audio is recorded locally.
5. **End the call** (interviewer only) — choose whether to run AI evaluation.
6. **Review results** — both participants can view scores and feedback from the dashboard.

## Project Structure

```
Fair-View/
├── python/                  # FastAPI backend
│   ├── app.py               # Main application & endpoints
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── security.py          # JWT & password hashing
│   ├── database.py          # Database engine & session
│   ├── init_db.py           # Database initialisation script
│   └── requirements.txt
├── frontend-video/
│   ├── src/
│   │   ├── App.js           # Root component & routing
│   │   ├── AuthView.js      # Sign in / sign up
│   │   ├── DashboardView.js # Room list & management
│   │   ├── InterviewRoom.js # WebRTC call & recording
│   │   ├── ResultsView.js   # Score review & polling
│   │   ├── config.js        # Environment config
│   │   ├── utils.js         # Shared helpers
│   │   └── Icons.js         # SVG icons
│   ├── server/
│   │   └── server.js        # Node audio relay to Python
│   └── public/
└── README.md
```

## Security Notes

- **Never commit `.env` files** — they are in `.gitignore`
- Set a strong `JWT_SECRET_KEY` in production
- Restrict `ALLOWED_ORIGINS` to your frontend domain in production
- The default SQLite database is for development; use PostgreSQL for production

## License

MIT License
