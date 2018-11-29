from .models import CeleryPhoneModel


def chunks(l, n):
    """for large files yield n-sized chunks from l"""
    for i in range(0, len(l), n):
        for z in l[i:i + n]:
            yield z


class Importer:
    def __init__(self, file_object):
        self.file_object = file_object
        self.model = CeleryPhoneModel()
        self.to_update = []

    def parse(self):
        pass

    def read_file(self):
        pass

    def validate_data(self, row):
        if row['number'] in self.to_update:
            return False

    def check_existing(self):
        self.to_update = [item for item in self.model.objects.values_list('number', flat=True)]

    def process_and_save(self):
        self.check_existing()
        # todo loop over csv data
