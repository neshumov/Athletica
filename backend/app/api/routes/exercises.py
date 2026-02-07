from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseOut

router = APIRouter(tags=["exercises"])


@router.get("/exercises", response_model=list[ExerciseOut])
def list_exercises(db: Session = Depends(get_db)) -> list[ExerciseOut]:
    rows = db.query(Exercise).order_by(Exercise.name.asc()).all()
    return [ExerciseOut.model_validate(r.__dict__) for r in rows]


@router.post("/exercises", response_model=ExerciseOut)
def create_exercise(payload: ExerciseCreate, db: Session = Depends(get_db)) -> ExerciseOut:
    row = Exercise(
        name=payload.name,
        exercise_type=payload.exercise_type,
        muscle_group=payload.muscle_group,
        equipment=payload.equipment,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return ExerciseOut.model_validate(row.__dict__)
