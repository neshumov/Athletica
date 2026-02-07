from __future__ import annotations

from pydantic import BaseModel


class ExerciseCreate(BaseModel):
    name: str
    exercise_type: str
    muscle_group: str
    equipment: str


class ExerciseOut(BaseModel):
    id: int
    name: str
    exercise_type: str
    muscle_group: str
    equipment: str
