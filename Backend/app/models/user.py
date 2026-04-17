from datetime import UTC, datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    profile: Mapped["Profile | None"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    trips: Mapped[list["Trip"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    matches_sent: Mapped[list["Match"]] = relationship(
        foreign_keys="Match.user1_id",
        back_populates="user1",
        cascade="all, delete-orphan",
    )
    matches_received: Mapped[list["Match"]] = relationship(
        foreign_keys="Match.user2_id",
        back_populates="user2",
        cascade="all, delete-orphan",
    )
    messages: Mapped[list["Chat"]] = relationship(
        back_populates="sender",
        cascade="all, delete-orphan",
    )
