from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Exercise(Base):
    __tablename__ = "exercise"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    exercise_type: Mapped[str] = mapped_column(String(16))
    muscle_group: Mapped[str] = mapped_column(String(64))
    equipment: Mapped[str] = mapped_column(String(64))
