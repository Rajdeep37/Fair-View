from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    role: str
    created_at: datetime


class AuthSignupIn(BaseModel):
    email: str
    password: str = Field(min_length=6)
    role: str


class AuthSigninIn(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class RoomCreateIn(BaseModel):
    name: Optional[str] = None
    job_role: str = Field(min_length=1, description="Target job role, e.g. Cloud Engineer")
    position: str = Field(min_length=1, description="Seniority level, e.g. Junior, Mid, Senior")


class RoomJoinIn(BaseModel):
    room_code: str


class RoomOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    code: str
    name: str
    job_role: str = ""
    position: str = ""
    interviewer_id: str
    candidate_id: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime


class InterviewOut(BaseModel):
    id: str
    room_id: str
    room_code: Optional[str] = None
    interviewer_id: str
    candidate_id: Optional[str] = None
    created_by_id: str
    audio_file: Optional[str] = None
    json_file: Optional[str] = None
    full_transcript: Optional[str] = None
    qa_pairs: list[dict[str, Any]] = Field(default_factory=list)
    evaluation_report: dict[str, Any] = Field(default_factory=dict)
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None