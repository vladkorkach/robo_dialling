from __future__ import absolute_import, unicode_literals
from robo_call.celery import app
import celery
from celery import task
from celery import shared_task
from .models import PhoneNumber, CallInfo


class TaskWrapper(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # exc (Exception) - The exception raised by the task.
        # args (Tuple) - Original arguments for the task that failed.
        # kwargs (Dict) - Original keyword arguments for the task that failed.
        print('{0!r} failed: {1!r}'.format(task_id, exc))

    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        pass


@shared_task()
def send_notifiction(*args, **kwargs):
    print(celery.current_task)
    print(celery.current_task.request.id)
    print("aaa")
# @app.task()
# def task_number_one(a, b):
#     print('asdfg')
#
#
# @shared_task()
# def send_notifiction(*args, **kwargs):
#     print(args)
#     print(kwargs)
#     numbers = PhoneNumber.objects.filter(id__in=args)
#     infos = []
#     for number in numbers:
#         print(number)
#         info = CallInfo(phone_dialed=number, time_before_hang=9)
#         infos.append(info)
#     CallInfo.objects.bulk_create(infos)
#     print(infos)


# @shared_task()
# def make_call(*args, **kwargs):
#     pass
