from celery import Celery
from main import run_crew
import os

celery_app = Celery(
    "worker",
    broker=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.environ.get("REDIS_URL", "redis://localhost:6379/0")
)

@celery_app.task
def analyze_blood_report_task(query: str, file_path: str):
    return run_crew(query, file_path)