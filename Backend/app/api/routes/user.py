from fastapi import APIRouter, Depends

from app.services.auth_service import get_current_user
from app.services.user_service import get_current_user_profile, get_test_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/test")
def test_user_route() -> dict[str, str]:
    return get_test_user()


@router.get("/me")
def read_current_user(
    current_user: dict[str, str] = Depends(get_current_user),
) -> dict[str, str]:
    return get_current_user_profile(current_user)
