from __future__ import annotations


from __future__ import annotations

from datetime import date

import pandas as pd
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.nutrition import NutritionDaily
from app.models.workout import Workout, WorkoutExercise
from app.models.whoop import WhoopDaily


def build_feature_frame(db: Session) -> pd.DataFrame:
    whoop_rows = db.query(WhoopDaily).all()
    nutrition_rows = db.query(NutritionDaily).all()
    workout_rows = db.query(Workout).all()
    exercise_rows = db.query(WorkoutExercise).all()

    whoop_df = pd.DataFrame(
        [
            {
                "date": r.date,
                "hrv": r.hrv,
                "resting_heart_rate": r.resting_heart_rate,
                "recovery_score": r.recovery_score,
                "strain": r.strain,
                "sleep_duration_minutes": r.sleep_duration_minutes,
                "sleep_efficiency": r.sleep_efficiency,
                "missing_flag": r.missing_flag,
            }
            for r in whoop_rows
        ]
    )
    nutrition_df = pd.DataFrame(
        [
            {
                "date": r.date,
                "calories": r.calories,
                "protein_g": r.protein_g,
                "fat_g": r.fat_g,
                "carbs_g": r.carbs_g,
            }
            for r in nutrition_rows
        ]
    )
    workouts_df = pd.DataFrame(
        [
            {
                "id": r.id,
                "date": r.date,
                "duration_minutes": r.duration_minutes,
                "subjective_fatigue": r.subjective_fatigue,
                "workout_quality": r.workout_quality,
                "program_day_id": r.program_day_id,
            }
            for r in workout_rows
        ]
    )
    exercises_df = pd.DataFrame(
        [
            {
                "workout_id": r.workout_id,
                "exercise_type": r.exercise_type,
                "muscle_group": r.muscle_group or "Other",
                "equipment": r.equipment or "Other",
                "reps": r.reps,
                "weight_kg": r.weight_kg,
                "duration_minutes": r.duration_minutes,
            }
            for r in exercise_rows
        ]
    )

    if exercises_df.empty:
        exercise_features = pd.DataFrame(columns=["date"])
    else:
        exercises_df = exercises_df.merge(
            workouts_df[["id", "date"]], left_on="workout_id", right_on="id", how="left"
        )
        exercises_df["volume"] = exercises_df["reps"] * exercises_df["weight_kg"]
        strength_df = exercises_df[exercises_df["exercise_type"] == "strength"]
        cardio_df = exercises_df[exercises_df["exercise_type"] == "cardio"]

        strength_volume = (
            strength_df.groupby(["date", "muscle_group"])["volume"].sum().unstack(fill_value=0)
        )
        strength_volume.columns = [f"vol_{c.lower()}" for c in strength_volume.columns]

        cardio_minutes = (
            cardio_df.groupby(["date", "equipment"])["duration_minutes"].sum().unstack(fill_value=0)
        )
        cardio_minutes.columns = [f"cardio_{c.lower().replace(' ', '_')}" for c in cardio_minutes.columns]

        exercise_features = pd.concat([strength_volume, cardio_minutes], axis=1).reset_index()

    df = whoop_df.merge(nutrition_df, on="date", how="outer")
    if not exercise_features.empty:
        df = df.merge(exercise_features, on="date", how="outer")

    df = df.sort_values("date")
    df = df.fillna(0)
    return df


def train_all_models() -> dict:
    db = SessionLocal()
    try:
        features = build_feature_frame(db)
        return {
            "recovery_model": "not_trained",
            "progress_model": "not_trained",
            "volume_model": "not_trained",
            "feature_rows": int(features.shape[0]),
            "feature_columns": int(features.shape[1]),
        }
    finally:
        db.close()
