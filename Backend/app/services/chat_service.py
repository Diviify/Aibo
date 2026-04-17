from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat import Chat


def create_message(match_id: int, sender_id: int, message: str, db: Session) -> Chat:
    chat_message = Chat(
        match_id=match_id,
        sender_id=sender_id,
        message=message,
    )
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    return chat_message


def get_messages(match_id: int, db: Session) -> list[Chat]:
    statement = (
        select(Chat)
        .where(Chat.match_id == match_id)
        .order_by(Chat.created_at.asc(), Chat.id.asc())
    )
    return list(db.execute(statement).scalars().all())
