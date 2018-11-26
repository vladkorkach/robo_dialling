from __future__ import absolute_import, unicode_literals
from robo_call.celery import app, test
from celery import task
from celery import shared_task

@app.task()
def task_number_one(a, b):
    print('asdfg')
#
#
# @app.on_after_configure.connect
# def set_up_periodic_tasks(sender, **kwargs):
#     # pass
#     sender.add_periodic_task(10.0, test.s('hello'))


# @app.task()
# def some_celery_task():
#     result = celery_task
@shared_task()
def send_notifiction():
     print('Here I\’m')
     # Another trick
