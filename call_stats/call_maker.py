from twilio.rest import Client
from .models import TwilioSetting


class TwilioConnecter:
    def __init__(self):
        self.auth_token = ""
        self.sid = ""
        self.client = Client(self.sid, self.auth_token)
        self.root_url = "https://api.twilio.com/"

    def get_balance(self):
        pass


class TwilioCaller:
    def __init__(self, user_id):
        self.user_id = user_id
        self.settings = self.prepare_settings()

    def prepare_settings(self):
        settings = TwilioSetting.objects.filter(user__pk=self.user_id).first()
        return settings

    def make_call(self):
        return self.settings
