from __future__ import annotations

from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CalendarWorkout(Base):
    __tablename__ = "calendar_workout"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date)
    workout_template_id: Mapped[int] = mapped_column(ForeignKey("workout_template.id"))
    name_snapshot: Mapped[str] = mapped_column(String(128))


class CalendarWorkoutExercise(Base):
    __tablename__ = "calendar_workout_exercise"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    calendar_workout_id: Mapped[int] = mapped_column(ForeignKey("calendar_workout.id"))
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercise.id"))
    exercise_name: Mapped[str] = mapped_column(String(128))
    exercise_type: Mapped[str] = mapped_column(String(16))
    muscle_group: Mapped[str] = mapped_column(String(64))
    equipment: Mapped[str] = mapped_column(String(64))
    set_number: Mapped[int] = mapped_column(Integer)
    reps: Mapped[int | None] = mapped_column(Integer)
    weight_kg: Mapped[float | None] = mapped_column(Float)
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
