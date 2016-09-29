# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django

django.setup()

from django.test import TestCase
from django.core import serializers

from easy_fixture.easy_fixture import EasyFixture

from . import fixtures_template


class EasyFixturesTest(TestCase):

    def test_fixtures(self):
        ef = EasyFixture(fixtures_template.fixtures_template)
        serializer_data = ef.output()
        deser_gens = list(serializers.deserialize('json', json.dumps(serializer_data)))
        for gen in deser_gens:
            gen.save()
        fixture_models = sorted([i for i in deser_gens if i.object.__class__.__name__ == 'FixtureModel'], key=lambda key: key.object.pk)
        foreign_models = sorted([i for i in deser_gens if i.object.__class__.__name__ == 'FixtureForeignModel'], key=lambda key: key.object.pk)
        manytomany_models = sorted([i for i in deser_gens if i.object.__class__.__name__ == 'FixtureManyToManyModel'], key=lambda key: key.object.pk)

        fixture_models_datas = [{'info': {'pk': 1, 'char_field': '1', 'integer_field': 2, 'url': '1',
                                          'unique_together_char_field_one': '1',
                                          'unique_together_char_field_two': '1'},
                                 'foreign_field': 1, 'many_to_many': [1, 2], 'bin': '1'
                                 },
                                {'info': {'pk': 2, 'char_field': '2', 'integer_field': 1, 'url': '2',
                                          'unique_together_char_field_one': '2', 'unique_together_char_field_two': '2'},
                                 'foreign_field': 2, 'many_to_many': [], 'bin': '2'
                                 }]

        for data_index in range(2):
            for i in fixture_models_datas[data_index]['info']:
                self.assertEqual(str(getattr(fixture_models[data_index].object, i)), str(fixture_models_datas[data_index]['info'][i]))
            for rel in ['foreign_field']:
                self.assertEqual(getattr(fixture_models[data_index].object, rel).pk, fixture_models_datas[data_index][rel])
            for m2m in ['many_to_many']:
                self.assertEqual(list(getattr(fixture_models[data_index].object, m2m).values_list('pk', flat=True)), fixture_models_datas[data_index][m2m])
            bin_data = bytes(fixture_models[data_index].object.bin).decode('utf-8')
            self.assertEqual(bin_data, fixture_models_datas[data_index]['bin'])

        foreign_models_datas = [{'pk': 1, 'postive_integer': 1, 'postive_small_integer': 1, 'file_path_field': '1', 'float_field': 1.0, 'ip': '1', 'slug_field': '1',
                                 'small_in': 1, 'text_field': '1'},
                                {'pk': 2, 'postive_integer': 2, 'postive_small_integer': 2, 'file_path_field': '2', 'float_field': 2.0, 'ip': '2', 'slug_field': '2',
                                 'small_in': 2, 'text_field': '2'}]
        for data_index in range(2):
            for f in ['pk', 'postive_integer', 'postive_small_integer', 'file_path_field', 'float_field', 'ip', 'slug_field', 'small_in', 'text_field']:
                self.assertEqual(getattr(foreign_models[data_index].object, f), foreign_models_datas[data_index][f])

        manytomany_models_datas = [{'pk': 1, 'biginteger_field': 3, 'boolean_field': True, 'non_boolean_field': None, 'comma_sep_field': '1',
                                    'duration_field': '0:00:01', 'email': '1'},
                                   {'pk': 2, 'biginteger_field': 4, 'boolean_field': True, 'non_boolean_field': None, 'comma_sep_field': '2',
                                    'duration_field': '0:00:02', 'email': '2'},
                                   ]
        for data_index in range(2):
            for f in ['pk', 'biginteger_field', 'boolean_field', 'non_boolean_field', 'comma_sep_field', 'duration_field', 'email']:
                self.assertEqual(str(getattr(manytomany_models[data_index].object, f)), str(manytomany_models_datas[data_index][f]))

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'test', 'testapp.tests.%s' % os.path.basename(__file__).split('.')[0]])
