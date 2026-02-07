from __future__ import annotations

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "athletica",
    broker=settings.redis_url,
    backend=settings.redis_url,
)
celery_app.conf.task_routes = {
    "app.workers.tasks.sync_whoop": {"queue": "whoop"},
    "app.workers.tasks.train_models": {"queue": "ml"},
}
