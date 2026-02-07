from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.workout import Workout, WorkoutExercise
from app.schemas.workout import WorkoutCreate

router = APIRouter(tags=["workouts"])


@router.post("/workouts")
def create_workout(payload: WorkoutCreate, db: Session = Depends(get_db)) -> dict:
    workout = Workout(
        date=payload.date,
        duration_minutes=payload.duration_minutes,
        subjective_fatigue=payload.subjective_fatigue,
        workout_quality=payload.workout_quality,
    )
    db.add(workout)
    db.flush()

    for ex in payload.exercises:
        db.add(
            WorkoutExercise(
                workout_id=workout.id,
                exercise_name=ex.exercise_name,
                set_number=ex.set_number,
                reps=ex.reps,
                weight_kg=ex.weight_kg,
                rpe=ex.rpe or 0.0,
            )
        )

    db.commit()
    return {"id": workout.id}
