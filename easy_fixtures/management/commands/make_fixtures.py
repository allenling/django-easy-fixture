# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
import importlib

from django.core.management.base import BaseCommand

from easy_fixtures.easy_fixtures import EasyFixture


class Command(BaseCommand):
    help = 'create a minimum useful fixture by a fixture template'

    def add_arguments(self, parser):
        parser.add_argument('template', help='fixture template file path')

    def handle(self, *args, **options):
        tem = importlib.import_module(options['template'])
        ef = EasyFixture(tem.fixtures_template)
        self.stdout.write(ef.output())
