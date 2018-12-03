from .models import CeleryPhoneModel
import pandas as pd


def chunks(l, n):
    """for large files yield n-sized chunks from l"""
    for i in range(0, len(l), n):
        for z in l[i:i + n]:
            yield z


class Exporter:
    def __init__(self, file_object):
        self.file_object = file_object
        self.model = CeleryPhoneModel()
        self.to_update = []
        self.df = []
        self.read_file()
        data = self.parse()
        self.process_and_save(data)

    @property
    def names(self):
        headers = [
            "Organization",
            "Department",
            "Purpose",
            "Phone Number"
        ]

        return headers

    def parse(self):
        print(self.df)
        for row in self.df:
            print(self.df[row])
        data = self.df.to_dict('records')
        print(data)
        return data

    def read_file(self):
        try:
            self.df = pd.read_csv(self.file_object)
        except BaseException:
            print(Exception.args)

    def validate_data(self, row):
        if row['number'] in self.to_update:
            return False

    def check_existing(self):
        self.to_update = [item for item in self.model.objects.values_list('number', flat=True)]

    def process_and_save(self, data):
        self.check_existing()
        # todo loop over csv data
