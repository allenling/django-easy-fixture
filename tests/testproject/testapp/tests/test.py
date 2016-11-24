# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

from django.test import TestCase
from django.db.models import fields as django_fields

from easy_fixture.easy_fixture import EasyFixture

from testapp import models

FIXTURE_DICT = {'testapp.FixtureModel': [{'pk': 1, 'char_field': '1', 'many_to_many': [1, 2]},
                                         {'pk': 2, 'integer_field': 1}],
                'testapp.FixtureManyToManyModel': [{'pk': 1, 'biginteger_field': 3}]
                }


class EasyFixturesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        ef = EasyFixture(FIXTURE_DICT)
        ef.load_into_testcase()
        TestCase.setUpTestData()

    def test_fixtures(self):
        fixture_models_datas = [{'fields': {'char_field': '1', 'integer_field': 2, 'url': '1',
                                            'unique_together_char_field_one': '1',
                                            'unique_together_char_field_two': '1'},
                                 'pk': 1,
                                 'foreign_field': 1, 'many_to_many': [1, 2], 'bin': '1'
                                 },
                                {'fields': {'char_field': '2', 'integer_field': 1, 'url': '2',
                                            'unique_together_char_field_one': '2', 'unique_together_char_field_two': '2'},
                                 'pk': 2,
                                 'foreign_field': 2, 'many_to_many': [], 'bin': '2'
                                 }]

        for data_index in range(2):
            obj_data = fixture_models_datas[data_index]
            obj = models.FixtureModel.objects.get(pk=obj_data['pk'])
            for i in obj_data['fields']:
                self.assertEqual(getattr(obj, i), obj_data['fields'][i])
            for rel in ['foreign_field']:
                self.assertEqual(getattr(obj, rel).pk, obj_data[rel])
            for m2m in ['many_to_many']:
                self.assertEqual(list(getattr(obj, m2m).values_list('pk', flat=True)), obj_data[m2m])
            bin_data = bytes(obj.bin).decode('utf-8')
            self.assertEqual(bin_data, obj_data['bin'])

        foreign_models_datas = [{'fields': {'postive_integer': 1, 'postive_small_integer': 1, 'file_path_field': '1', 'float_field': 1.0, 'ip': '1', 'slug_field': '1',
                                            'small_in': 1, 'text_field': '1'},
                                 'pk': 1},
                                {'fields': {'postive_integer': 2, 'postive_small_integer': 2, 'file_path_field': '2', 'float_field': 2.0, 'ip': '2', 'slug_field': '2',
                                            'small_in': 2, 'text_field': '2'},
                                 'pk': 2}
                                ]
        for data_index in range(2):
            obj_data = foreign_models_datas[data_index]
            obj = models.FixtureForeignModel.objects.get(pk=obj_data['pk'])
            for f in obj_data['fields']:
                self.assertEqual(getattr(obj, f), obj_data['fields'][f])

        manytomany_models_datas = [{'fields': {'biginteger_field': 3, 'boolean_field': True, 'non_boolean_field': None, 'comma_sep_field': '1',
                                               'email': '1'},
                                    'pk': 1,
                                    'duration_field': '0:00:01',
                                    },
                                   {'fields': {'biginteger_field': 4, 'boolean_field': True, 'non_boolean_field': None, 'comma_sep_field': '2',
                                               'email': '2'},
                                    'pk': 2,
                                    'duration_field': '0:00:02',
                                    }
                                   ]
        for data_index in range(2):
            obj_data = manytomany_models_datas[data_index]
            obj = models.FixtureManyToManyModel.objects.get(pk=obj_data['pk'])
            self.assertEqual(getattr(obj, 'duration_field'), django_fields.parse_duration(obj_data['duration_field']))
            for f in obj_data['fields']:
                self.assertEqual(getattr(obj, f), obj_data['fields'][f])
