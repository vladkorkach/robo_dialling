from __future__ import absolute_import, unicode_literals
from robo_call.celery import app, test
from celery import task
from celery import shared_task
from .models import PhoneNumber, CallInfo


@app.task()
def task_number_one(a, b):
    print('asdfg')


@shared_task()
def send_notifiction(*args, **kwargs):
    print(args)
    print(kwargs)
    numbers = PhoneNumber.objects.filter(id__in=args)
    infos = []
    for number in numbers:
        print(number)
        info = CallInfo(phone_dialed=number, time_before_hang=9)
        infos.append(info)
    CallInfo.objects.bulk_create(infos)
    print(infos)


# @shared_task()
# def make_call(*args, **kwargs):
#     pass
