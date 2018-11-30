from twilio.rest import Client
from .models import TwilioSettings


class TwilioCaller:
    def __init__(self):
        pass

    def prepare_settings(self):
        settings = TwilioSettings.objects.all()

    def make_call(self):
        pass
