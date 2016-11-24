django-easy-fixture
===================
.. figure:: https://travis-ci.org/allenling/django-easy-fixture.svg?branch=master

python2.7, python3.5

1.8<= Django <= 1.10

**install: pip install django-easy-fixture**

That is a easy, simple tool to help you to fill your fixture dict with some spam datas

Make your fixture dict to be a completely available django fixture that **you do not have to worry about any unqiue, unqie_together, just pk**

**The pk must be defined by you!**


1. get a fixture dict
---------------------

.. code-block:: python

   # in template.py
   fixtures_template={'auth.User': [{'pk': 1}]}

   # in other.py
   from easy_fixture.easy_fixture import EasyFixture
   from template import fixtures_template

   ef = EasyFixture(fixtures_template)
   fixtures_dict = ef.output()

2. use as a django app command
------------------------------

.. code-block:: python

   # in template.py
   fixtures_template={'auth.User': [{'pk': 1}]}

   # in your settings.py
   INSTALLED_APPS = ('other apps',
                     'easy_fixture',
                     )
run make_fixture command
 
.. code-block:: python

   python manage.py make_fixture template > /path/to/fixture.json

3. use in test
--------------

In your testCase, call EasyFixture.load_into_testcase in your setUpTestData, setUpClass or setUp.

.. code-block:: python

   class MyTestCase(TestCase):
       
       @classmethod
       def setUpTestData(cls):
           ef = EasyFixture(FIXTURE_DICT)
           ef.load_into_testcase()
           TestCase.setUpTestData()
       
       def tes_what_you_want(self):
           pass


**deprecate**

.. code-block:: python

   from easy_fixture.easy_fixture import FixtureFileGen

   class MyCase(TestCase):
      fixtures = FixtureFileGen(['my.fixture.template.module'])
