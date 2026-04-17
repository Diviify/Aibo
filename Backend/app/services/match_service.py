from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.user import User


def normalize_pair(user1_id: int, user2_id: int) -> tuple[int, int]:
    if user1_id <= user2_id:
        return user1_id, user2_id
    return user2_id, user1_id


def get_existing_match(user1_id: int, user2_id: int, db: Session) -> Match | None:
    normalized_user1_id, normalized_user2_id = normalize_pair(user1_id, user2_id)

    statement = select(Match).where(
        or_(
            (Match.user1_id == normalized_user1_id) & (Match.user2_id == normalized_user2_id),
            (Match.user1_id == normalized_user2_id) & (Match.user2_id == normalized_user1_id),
        )
    )
    return db.execute(statement).scalar_one_or_none()


def create_match(user1: User, user2: User, score: float, db: Session) -> Match:
    if user1.id == user2.id:
        raise ValueError("Users cannot match with themselves")

    normalized_user1_id, normalized_user2_id = normalize_pair(user1.id, user2.id)
    existing_match = get_existing_match(normalized_user1_id, normalized_user2_id, db)
    if existing_match is not None:
        return existing_match

    match = Match(
        user1_id=normalized_user1_id,
        user2_id=normalized_user2_id,
        score=score,
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match
