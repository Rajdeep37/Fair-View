import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, JSON, String, Text

from database import Base


def new_uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=new_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(32), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Room(Base):
    __tablename__ = "rooms"

    id = Column(String, primary_key=True, default=new_uuid)
    code = Column(String(32), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    job_role = Column(String(255), nullable=False, default="")
    position = Column(String(64), nullable=False, default="")
    interviewer_id = Column(String, ForeignKey("users.id"), nullable=False)
    candidate_id = Column(String, ForeignKey("users.id"), nullable=True)
    status = Column(String(32), nullable=False, default="waiting")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(String, primary_key=True, default=new_uuid)
    room_id = Column(String, ForeignKey("rooms.id"), nullable=False, index=True)
    interviewer_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    candidate_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    created_by_id = Column(String, ForeignKey("users.id"), nullable=False)
    audio_file = Column(String(512), nullable=True)
    json_file = Column(String(512), nullable=True)
    full_transcript = Column(Text, nullable=True)
    qa_pairs = Column(JSON, nullable=True)
    evaluation_report = Column(JSON, nullable=True)
    status = Column(String(32), nullable=False, default="completed")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)