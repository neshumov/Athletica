from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.calendar import CalendarWorkout, CalendarWorkoutExercise
from app.models.exercise import Exercise
from app.models.workout_template import WorkoutTemplate, WorkoutTemplateExercise
from app.schemas.calendar import CalendarWorkoutCreate, CalendarWorkoutOut

router = APIRouter(tags=["calendar"])


@router.get("/calendar", response_model=list[CalendarWorkoutOut])
def list_calendar(
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[CalendarWorkoutOut]:
    query = db.query(CalendarWorkout)
    if date_from:
        query = query.filter(CalendarWorkout.date >= date_from)
    if date_to:
        query = query.filter(CalendarWorkout.date <= date_to)
    rows = query.order_by(CalendarWorkout.date.desc()).all()
    return [CalendarWorkoutOut.model_validate(r.__dict__) for r in rows]


@router.post("/calendar", response_model=CalendarWorkoutOut)
def create_calendar(payload: CalendarWorkoutCreate, db: Session = Depends(get_db)) -> CalendarWorkoutOut:
    template = db.query(WorkoutTemplate).filter(WorkoutTemplate.id == payload.workout_template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    calendar = CalendarWorkout(
        date=payload.date,
        workout_template_id=template.id,
        name_snapshot=template.name,
    )
    db.add(calendar)
    db.flush()

    template_exercises = db.query(WorkoutTemplateExercise).filter(
        WorkoutTemplateExercise.workout_template_id == template.id
    ).all()
    template_map = {te.exercise_id: te for te in template_exercises}

    for ex in payload.exercises:
        exercise = db.query(Exercise).filter(Exercise.id == ex.exercise_id).first()
        if not exercise:
            raise HTTPException(status_code=404, detail=f"Exercise {ex.exercise_id} not found")
        db.add(
            CalendarWorkoutExercise(
                calendar_workout_id=calendar.id,
                exercise_id=exercise.id,
                exercise_name=exercise.name,
                exercise_type=exercise.exercise_type,
                muscle_group=exercise.muscle_group,
                equipment=exercise.equipment,
                set_number=ex.set_number,
                reps=ex.reps,
                weight_kg=ex.weight_kg,
                duration_minutes=ex.duration_minutes,
            )
        )

    db.commit()
    return CalendarWorkoutOut.model_validate(calendar.__dict__)
