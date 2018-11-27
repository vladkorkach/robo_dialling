from __future__ import absolute_import, unicode_literals
import celery
from celery import shared_task
import random
from .models import CeleryPhoneModel, CallStat


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


@shared_task(name='TwilioCaller', base=TaskWrapper)
def make_twilio_call(*args, **kwargs):
    numbers = CeleryPhoneModel.objects.filter(id__in=args)
    infos = []

    for number in numbers:
        info = CallStat(phone_dialed=number, time_before_hang=random.randint(0, 9))
        infos.append(info)

    CallStat.objects.bulk_create(infos)
