from datetime import datetime

from twilio.rest import Client
from .models import TwilioSetting
from robo_call.settings import TWILIO_AUTH_TOKEN, TWILIO_SID, TWILIO_ROOT_URL


class TwilioConnecter:
    def __init__(self):
        self.auth_token = TWILIO_AUTH_TOKEN
        self.sid = TWILIO_SID
        self.client = Client(self.sid, self.auth_token)
        self.root_url = TWILIO_ROOT_URL
        self.account = self.client.api.accounts(self.sid).fetch()

    def get_balance(self):
        data = self.account.balance.fetch()
        return data.balance

    def get_calls_list(self, **kwargs):
        if 'start_time_after' in kwargs and 'start_time_before' in kwargs:
            after = datetime.strptime(kwargs["start_time_after"], "%Y-%m-%d")
            before = datetime.strptime(kwargs["start_time_before"], "%Y-%m-%d")
            call_list = self.account.calls.list(start_time_after=datetime(after.year, after.month, after.day, 0, 0),
                                                start_time_before=datetime(before.year, before.month, before.day, 0, 0))
        else:
            call_list = self.account.calls.list()
        calls_list_info = []
        for c in call_list:
            print(c.date_created, c.date_updated, c.duration, c.end_time, c.start_time)
            print("!!", c.end_time - c.start_time)
            tmp = {
                "sid": c.sid,
                "duration": c.duration,
                "price": c.price,
                "status": c.status,
                "start_time": c.start_time,
                "end_time": c.end_time,
                "to": c.to
            }
            calls_list_info.append(tmp)
        return calls_list_info

    def get_call_info(self, sid):
        return self.client.calls(sid).fetch()


class TwilioCaller:
    def __init__(self, client: Client):
        self.client = client

    def make_call(self):
        call = self.client.calls.create(
            method="GET",
            status_callback="",
            status_callback_event=["answered", "completed"],
            status_callback_method="POST",
            url="",
            to="",
            from_=""
        )
        print(call.sid)
