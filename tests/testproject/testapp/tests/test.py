from django.test import TestCase

from easy_fixture.easy_fixture import EasyFixture

from testapp import models

FIXTURE_DICT = {'testapp.FixtureModel': [{'pk': 1, 'char_field': 'abcd', 'many_to_many': [1, 2]},
                                         {'pk': 2, 'integer_field': 100},
                                         {'pk': 3, 'foreign_field': 1},
                                         ],
                'testapp.FixtureForeignModel': [{'pk': 1},
                                                ],
                'testapp.FixtureManyToManyModel': [{'pk': 1, 'biginteger_field': 3}]
                }


class EasyFixturesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        ef = EasyFixture(FIXTURE_DICT)
        ef.save()
#         ef.save_file()
        return TestCase.setUpTestData()

    def test_fixtures(self):
        for i in models.FixtureModel.objects.all():
            print(i.id, i.foreign_field.id)
        print('------------')
        print(models.FixtureForeignModel.objects.count())
        print(models.FixtureManyToManyModel.objects.count())
        return
