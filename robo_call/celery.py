from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
# import call_stats.tasks


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'robo_call.settings')

app = Celery('robo_call')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task
def test(arg):
    print(arg)


app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'call_stats.tasks.task_number_one',
        'schedule': 30.0,
        'args': (16, 16)
    },
}
app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
