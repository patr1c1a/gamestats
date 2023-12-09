import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exercise.settings")
app = Celery("exercise")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Periodic task
app.conf.beat_schedule = {
    'run-simulate-stats-periodically': {
        'task': 'game_stats.tasks.simulate_stats_task',
        'schedule': crontab(minute='*/5'),
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
