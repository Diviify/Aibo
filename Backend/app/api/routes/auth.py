from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import TokenResponse
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import authenticate_user, create_mock_user, create_user_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate) -> dict[str, str]:
    try:
        create_mock_user(user_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return {"message": "User created successfully"}


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin) -> TokenResponse:
    user = authenticate_user(credentials.email, credentials.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return create_user_token(user.email)
