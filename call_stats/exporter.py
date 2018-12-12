from .models import CeleryPhoneModel
from django_celery_beat.models import IntervalSchedule
import pandas as pd


def chunks(l, n):
    """for large files yield n-sized chunks from l"""
    for i in range(0, len(l), n):
        for z in l[i:i + n]:
            yield z


class Exporter:
    def __init__(self, file_object):
        self.file_object = file_object
        self.model = CeleryPhoneModel
        self.to_update = []
        self.df = []
        self.data_as_dict = []
        self.read_file()
        self.parse_and_convert()
        self.process_and_save()

    def parse_and_convert(self):
        data = self.df.to_dict('records')
        self.data_as_dict = data

    def read_file(self):
        try:
            self.df = pd.read_csv(self.file_object)
        except BaseException:
            print(Exception.args)

    def validate_data(self, row):
        if row['number'] in self.to_update:
            return False

    def check_existing(self, row):
        self.to_update = [item for item in self.model.objects.values_list('number', flat=True)]
        valid = True
        if str(row) in self.to_update:
            valid = False

        return valid

    def process_and_save(self):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS
        )

        for d in self.data_as_dict:
            valid = self.check_existing(d)
            if not valid:
                continue

            try:
                self.model.objects.create(
                    interval=schedule,
                    name="call {}".format(str(d["Phone number"])),
                    task="TwilioCaller",
                    enabled=False,
                    number=str(d["Phone number"]),
                    organization=d["Organisation"],
                    department=d["Department"],
                    purpose=d["Purpose"]
                )

            except Exception as e:
                print(e.args)
