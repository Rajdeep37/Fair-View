import os
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "720"))

if SECRET_KEY == "dev-secret-change-me":
    import warnings
    warnings.warn(
        "JWT_SECRET_KEY is not set — using insecure default. "
        "Set JWT_SECRET_KEY in your .env for production.",
        stacklevel=1,
    )

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(subject: str, claims: dict | None = None) -> str:
    payload = {"sub": subject, "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
    if claims:
        payload.update(claims)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def parse_bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise ValueError("Missing authorization header")
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        raise ValueError("Authorization header must use Bearer scheme")
    return authorization[len(prefix):].strip()