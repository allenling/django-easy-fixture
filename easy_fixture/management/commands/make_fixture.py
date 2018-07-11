import importlib
import json

from django.core.management.base import BaseCommand

from easy_fixture.easy_fixture import EasyFixture


class Command(BaseCommand):
    help = 'create a available fixture with a simple model dict'

    def add_arguments(self, parser):
        parser.add_argument('fixture_path', help='')

    def handle(self, *args, **options):
        fixture_path = options['fixture_path']
        fpath, fixture_var_name = fixture_path.rsplit('.', 1)
        fpath = importlib.import_module(fpath)
        fixture_var = getattr(fpath, fixture_var_name)
        ef = EasyFixture(fixture_var)
        self.stdout.write(json.dumps(ef.output()))
        return
