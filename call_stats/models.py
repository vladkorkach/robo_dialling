from django.db import models
from django.contrib.auth.models import User
from django_celery_beat.models import PeriodicTask
import os
import signal


class CeleryPhoneModel(PeriodicTask):
    number = models.CharField(max_length=14, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    purpose = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.task = "TwilioCaller"

        self.exchange = self.exchange or None
        self.routing_key = self.routing_key or None
        self.queue = self.queue or None
        if not self.enabled:
            self.last_run_at = None

        # F = open("celerybeat.pid", "r")
        # ppid = int(F.readline())
        # os.kill(ppid, signal.SIGTERM)  # or signal.SIGKILL
        #
        # cmd = 'celery -A robo_call beat -l DEBUG --scheduler django_celery_beat.schedulers:DatabaseScheduler -f robo_call.log &'
        # os.system(cmd)

        # celery -A robo_call beat -l DEBUG --scheduler django_celery_beat.schedulers:DatabaseScheduler -f robo_call.log
        if not self.pk:
            super(CeleryPhoneModel, self).save(*args, **kwargs)
            self.args = [self.pk]
            super(CeleryPhoneModel, self).save(*args, **kwargs)
        else:
            self.args = [self.pk]
            super(CeleryPhoneModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.number


class CallStat(models.Model):
    phone_dialed = models.ForeignKey(CeleryPhoneModel, null=True, blank=True, on_delete=models.CASCADE)
    time_before_hang = models.IntegerField()
    phone_is_active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_dialed.number


class TwilioSettings(models.Model):
    pass
