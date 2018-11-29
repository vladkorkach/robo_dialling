from __future__ import absolute_import, unicode_literals
import celery
from celery import shared_task, task
import random
from .models import CeleryPhoneModel, CallStat
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='robo_call.log',
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


# TODO logs
class TaskWrapper(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # exc (Exception) - The exception raised by the task.
        # args (Tuple) - Original arguments for the task that failed.
        # kwargs (Dict) - Original keyword arguments for the task that failed.
        msg = '{0!r} failed: {1!r} args:{2!}'.format(task_id, exc, str(args))
        logging.error(msg)

    def on_success(self, retval, task_id, args, kwargs):
        msg = '{0!r} success: {1!r}'.format(task_id, str(args))
        logging.info(msg)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        msg = 'RETRY {0!r} failed: {1!r} args:{2!}'.format(task_id, exc, str(args))
        logging.info(msg)


@shared_task(name='TwilioCaller', base=TaskWrapper)
def make_twilio_call(*args, **kwargs):
    numbers = CeleryPhoneModel.objects.filter(id__in=args)
    infos = []

    for number in numbers:
        info = CallStat(phone_dialed=number, time_before_hang=random.randint(0, 9))
        infos.append(info)

    CallStat.objects.bulk_create(infos)
