# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
import importlib
import json

from django.core.management.base import BaseCommand

from easy_fixture.easy_fixture import EasyFixture


class Command(BaseCommand):
    help = 'create a available fixture with a simple model dict'

    def add_arguments(self, parser):
        parser.add_argument('template', help='fixture module path')

    def handle(self, *args, **options):
        tem = importlib.import_module(options['template'])
        ef = EasyFixture(tem.fixtures_template)
        self.stdout.write(json.dumps(ef.output()))
