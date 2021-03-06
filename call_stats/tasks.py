from __future__ import absolute_import, unicode_literals

import json
import random

import celery
from celery import shared_task
from .models import CeleryPhoneModel, CallStat
import logging
from django.utils import timezone
from .call_maker import TwilioCaller, TwilioConnecter
from .helpers import randomDate


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


class TaskWrapper(celery.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
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
    """
    task, created from CeleryPhoneModel
    :param args:
    :param kwargs:
    :return:
    """
    numbers = CeleryPhoneModel.objects.filter(id__in=args)
    # infos = []
    connecter = TwilioConnecter()
    caller = TwilioCaller(connecter.client)

    for number_model in numbers:
        data = caller.make_call(number=number_model.number)

        if data[0]:
            call_stat = CallStat(phone_dialed=number_model, time_before_hang=0, sid=data[0].sid, status=data[0].status)
        else:
            stat = True
            if data[1].phone_status:
                stat = False
            debug_info = json.dumps(data[1].__dict__)
            call_stat = CallStat(phone_dialed=number_model, debug_info=debug_info, time_before_hang=0, phone_is_active=stat, sid=None, status="wrong")

        call_stat.save()


@shared_task(name="SyncWithTwilioStats")
def sync_with_twilio_stats(*args, **kwargs):
    """
    uses for synchronizing twilio statistics with our databases
    if twilio callbacks don't work, launch this task as usual celery periodic task
    :param args: usual celery args
    :param kwargs: usual celery kwargs
    :return: None, writes changed call info into database
    """
    connecter = TwilioConnecter()
    today = timezone.now().date()

    data = CallStat.objects.filter(status="queued").last()
    from_ = data.date.strftime('%Y-%m-%d')
    today = today.strftime('%Y-%m-%d')

    kw = {"start_time_after": from_, "start_time_before": today}
    calls = None
    try:
        calls = connecter.get_calls_list(**kw)
        print(calls)
    except Exception as e:
        print(e.args)

    for c in calls:
        call_stat = CallStat.objects.filter(sid=c["sid"]).first()
        if call_stat:
            call_stat.time_before_hang = c["duration"]
            call_stat.status = c["status"]

            call_stat.save()


@shared_task(name="GenerateFakeData")
def generate_fake_data(*args, **kwargs):
    """
    Generate some fake data
    :param args:
    :param kwargs:
    :return:
    """
    numbers = CeleryPhoneModel.objects.all()
    statuses = ["wrong", "completed", "queued", "no-answer", "canceled", "failed", "in-progress"]
    for number in numbers:
        date = randomDate("2018-12-09", "2018-12-09", random.random())

        call_stat = CallStat(phone_dialed=number, time_before_hang=random.randint(0, 14), sid="", status=statuses[random.randint(0, len(statuses)-1)], date=date)
        call_stat.save()
