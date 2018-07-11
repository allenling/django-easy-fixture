import django
from django.core.management.commands.loaddata import Command as LoadDataCommand


class DjangoLoadData(LoadDataCommand):
    '''
    support django > 2.x
    '''

    def set_fixture_data(self, data):
        self.fixture_data = data
        return

    def parse_name(self, fixture_file):
        self.compression_formats['easy_fixture'] = (self.open_method, 'rb',)
        return None, 'json', 'easy_fixture'

    def open_method(self, fixture_file, mode):
        return self.fixture_data

    def find_fixtures(self, fixture_label):
        return [['./fixture.json', '.', 'fixture']]


def save_to_db(fixture_data):
    django_version = django.__version__
    if django_version.startswith('2.'):
        dld = DjangoLoadData()
        dld.set_fixture_data(fixture_data)
        dld.run_from_argv(['manage.py', 'loaddata', 'fixture.json'])
    else:
        pass
    return
