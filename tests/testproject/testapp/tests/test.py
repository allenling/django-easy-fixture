# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
import json
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

        fixture_models_datas = [{'pk': 1, 'char_field': '1', 'integer_field': 2, 'foreign_field': 1, 'many_to_many': [1, 2]},
                                {'pk': 2, 'char_field': '2', 'integer_field': 1, 'foreign_field': 2, 'many_to_many': []}]
        for data_index in range(2):
            for f in ['pk', 'char_field', 'integer_field']:
                self.assertEqual(getattr(fixture_models[data_index].object, f), fixture_models_datas[data_index][f])
            for rel in ['foreign_field']:
                self.assertEqual(getattr(fixture_models[data_index].object, rel).pk, fixture_models_datas[data_index][rel])
            for m2m in ['many_to_many']:
                self.assertEqual(list(getattr(fixture_models[data_index].object, m2m).values_list('pk', flat=True)), fixture_models_datas[data_index][m2m])

        foreign_models_datas = [{'pk': 1, 'postive_integer': 1, 'postive_small_integer': 1},
                                {'pk': 2, 'postive_integer': 2, 'postive_small_integer': 2}]
        for data_index in range(2):
            for f in ['pk', 'postive_integer', 'postive_small_integer']:
                self.assertEqual(getattr(foreign_models[data_index].object, f), foreign_models_datas[data_index][f])

        manytomany_models_datas = [{'pk': 1, 'biginteger_field': 3},
                                   {'pk': 2, 'biginteger_field': 4},
                                   ]
        for data_index in range(2):
            for f in ['pk', 'biginteger_field']:
                self.assertEqual(getattr(manytomany_models[data_index].object, f), manytomany_models_datas[data_index][f])
