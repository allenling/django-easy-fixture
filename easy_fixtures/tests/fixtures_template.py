# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
fixtures_template = {'easy_fixtures.FixtureModel': [{'pk': 1, 'char_field': '1', 'many_to_many': [1, 2]},
                                                    {'pk': 2, 'integer_field': 1}],
                     'easy_fixtures.FixtureForeignModel': [{'pk': 1}],
                     'easy_fixtures.FixtureManyToManyModel': [{'pk': 1, 'biginteger_field': 3}]
                     }
