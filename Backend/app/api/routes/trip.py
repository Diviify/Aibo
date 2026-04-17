from fastapi import APIRouter

from app.services.trip_service import get_trip_placeholder

router = APIRouter(prefix="/trips", tags=["trips"])


@router.get("")
def list_trips() -> dict[str, str]:
    return get_trip_placeholder()
