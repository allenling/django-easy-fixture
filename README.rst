django-easy-fixtures
====================

easy to create a django fixtures with a fixture dict

create a fixture dict that just include some fields you concern, and we will help you to expand your fixture dict to a completely available django fixture

1. output a fixture dict
~~~~~~~~~~~~~~~~~~~~~~~~

in template.py

.. code-block:: python

   fixtures_template={'auth.User': [{'pk': 1}]}

then

.. code-block:: python

   from easy_fixtures.easy_fixtures import EasyFixture
   from template import fixtures_template

   ef = EasyFixture(fixtures_template)
   fixtures_dict = ef.output()

2. use as command
-----------------

2.1. create a simple fixture template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

in template.py

.. code-block:: python

   fixtures_template={'auth.User': [{'pk': 1}]}

2.2. in settings.py
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   INSTALLED_APPS = ('other apps',
                     'easy_fixtures',
                     )

2.3. run command
~~~~~~~~~~~~~~~~
 
.. code-block:: python


   python manage.py make_fixtures template > /path/to/fixture.json

3. use in test
--------------

.. code-block:: python

   from easy_fixtures.easy_fixtures import FixtureFileGen

   class MyCase(TestCase):
      fixtures = FixtureFileGen(['my.fixture.template.module'])
