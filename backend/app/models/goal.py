from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserGoal(Base):
    __tablename__ = "user_goal"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    goal_type: Mapped[str] = mapped_column(String(16))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    priority_muscle_groups: Mapped[list[str] | None] = mapped_column(JSON)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
