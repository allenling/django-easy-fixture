# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
import os
import sys
import json
sys.path.append('/opt/django-easy-fixtures')
os.environ['DJANGO_SETTINGS_MODULE'] = 'easy_fixtures.testproject.settings'
from django.test import TestCase
from django.core import serializers

from easy_fixtures.easy_fixtures import EasyFixture

from . import fixtures_template


class EasyFixturesTest(TestCase):

    def test_fixtures(self):
        ef = EasyFixture(fixtures_template.fixtures_template)
        deser_gens = list(serializers.deserialize('json', json.dumps(ef.output())))


if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'test', 'easy_fixtures.tests.%s' % os.path.basename(__file__).split('.')[0]])
