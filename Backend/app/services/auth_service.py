from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.models.user import User
from app.schemas.auth import TokenResponse
from app.schemas.user import UserCreate
from app.utils.security import hash_password, verify_password

security_scheme = HTTPBearer()
mock_users: dict[str, User] = {}


def create_mock_user(user_data: UserCreate) -> User:
    if user_data.email in mock_users:
        raise ValueError("User already exists")

    user = User(email=user_data.email, hashed_password=hash_password(user_data.password))
    mock_users[user.email] = user
    return user


def authenticate_user(email: str, password: str) -> User | None:
    user = mock_users.get(email)
    if user is None:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def create_access_token(subject: str) -> str:
    expire_at = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expire_at}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def verify_token(token: str) -> dict[str, str]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc

    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    return {"email": email}


def create_user_token(email: str) -> TokenResponse:
    access_token = create_access_token(email)
    return TokenResponse(access_token=access_token)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
) -> dict[str, str]:
    return verify_token(credentials.credentials)
