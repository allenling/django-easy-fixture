django-easy-fixtures
====================

easy to create a django fixtures with a fixture template dict

create a fixture dict that just include some fields you concern, and we will help you to expand your fixture dict to a completely useful django fixture

1. use as command
-----------------

1.1. create a simple fixture template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

in template.py

.. code-block:: python

   fixtures_template={'auth.User': [{'pk': 1}]}

1.2. create a full fixture
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python


   python manage.py make_fixtures template > /path/to/fixture.json

1.3. done
~~~~~~~~~

2. use in test
--------------

.. code-block:: python

   from easy_fixtures.easy_fixtures import FixtureFileGen

   class MyCase(TestCase):
      fixtures = FixtureFileGen(['my.fixture.template.module'])
