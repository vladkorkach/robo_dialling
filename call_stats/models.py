from django.db import models
from django.contrib.auth.models import User
from django_celery_beat.models import PeriodicTask, PeriodicTasks


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

        if not self.pk:
            super(CeleryPhoneModel, self).save(*args, **kwargs)
            self.args = [self.pk]
            super(CeleryPhoneModel, self).save(*args, **kwargs)
        else:
            self.args = [self.pk]
            super(CeleryPhoneModel, self).save(*args, **kwargs)
        PeriodicTasks.update_changed()

    def __str__(self):
        return self.number


class CallStat(models.Model):
    phone_dialed = models.ForeignKey(CeleryPhoneModel, null=True, blank=True, on_delete=models.CASCADE)
    time_before_hang = models.IntegerField()
    phone_is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    sid = models.CharField(max_length=255, null=True, blank=True)
    duration=models.CharField(max_length=255,null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_dialed.number


class TwilioSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, to_field='username', null=True, blank=True)
    account_sid = models.CharField(max_length=255, null=True, blank=True)
    auth_token = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    meta_data = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username
