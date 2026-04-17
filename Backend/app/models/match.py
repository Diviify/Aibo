from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="uq_matches_user_pair"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user1_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    user2_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    user1: Mapped["User"] = relationship(
        foreign_keys=[user1_id],
        back_populates="matches_sent",
    )
    user2: Mapped["User"] = relationship(
        foreign_keys=[user2_id],
        back_populates="matches_received",
    )
