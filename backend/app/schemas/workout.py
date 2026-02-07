from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field


class WorkoutExerciseIn(BaseModel):
    exercise_name: str
    set_number: int
    reps: int
    weight_kg: float
    rpe: float | None = None


class WorkoutCreate(BaseModel):
    date: date
    duration_minutes: int
    subjective_fatigue: int = Field(ge=1, le=10)
    workout_quality: str
    exercises: list[WorkoutExerciseIn]
