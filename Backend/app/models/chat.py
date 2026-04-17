from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), nullable=False, index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    match: Mapped["Match"] = relationship(back_populates="messages")
    sender: Mapped["User"] = relationship(back_populates="messages")
