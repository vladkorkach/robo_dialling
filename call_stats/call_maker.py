from datetime import datetime

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from robo_call.settings import TWILIO_AUTH_TOKEN, TWILIO_SID, TWILIO_ROOT_URL, BASE_URL, TWILIO_FROM_NUMBER


def test_check(func):
    def _decorator(self, *args, **kwargs):
        if self.test_mode:
            res = False
        else:
            res = func(self, *args, **kwargs)
        return res
    return _decorator


class TwilioConnecter:
    def __init__(self):
        self.test_mode = False
        self.auth_token = TWILIO_AUTH_TOKEN
        self.sid = TWILIO_SID
        self.client = Client(self.sid, self.auth_token)
        self.root_url = TWILIO_ROOT_URL
        self.account = self.get_account_info()

    @test_check
    def get_account_info(self):
        return self.client.api.accounts(self.sid).fetch()

    @test_check
    def get_balance(self):
        data = self.account.balance.fetch()
        return data.balance

    @test_check
    def get_calls_list(self, *args, **kwargs):

        if 'start_time_after' in kwargs and 'start_time_before' in kwargs:
            after = datetime.strptime(kwargs["start_time_after"], "%Y-%m-%d")
            before = datetime.strptime(kwargs["start_time_before"], "%Y-%m-%d")

            call_list = self.account.calls.list(start_time_after=datetime(after.year, after.month, after.day, 0, 0),
                                                start_time_before=datetime(before.year, before.month, before.day, 0, 0))
        else:
            call_list = self.account.calls.list()
        calls_list_info = []
        for c in call_list:
            tmp = {
                "sid": c.sid,
                "duration": c.duration,
                "price": c.price,
                "status": c.status,
                "start_time": c.start_time,
                "end_time": c.end_time,
                "to": c.to,
                "from_": c.from_,
            }
            calls_list_info.append(tmp)
        return calls_list_info

    @test_check
    def get_call_info(self, sid):
        return self.client.calls(sid).fetch()


class TwilioCaller:
    def __init__(self, client: Client):
        self.client = client

    def make_call(self, number):
        root_url = BASE_URL
        call = None
        err = None

        try:
            call = self.client.calls.create(
                method="GET",
                status_callback="{}call_stats/callback".format(root_url),
                status_callback_event=["answered", "completed"],
                status_callback_method="POST",
                url="http://demo.twilio.com/docs/voice.xml",
                to=number,
                from_=TWILIO_FROM_NUMBER,
                timeout=25
            )
        except TwilioRestException as e:
            if e.code in [21217, 21214, 21216]:
                e.__setattr__("phone_status", "invalid")
            err = e

        if not call:
            response = [None, err]
        else:
            response = [call, None]

        return response

    def synchronization(self):
        pass
