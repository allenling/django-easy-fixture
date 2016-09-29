django-easy-fixture
===================
.. figure:: https://travis-ci.org/allenling/django-easy-fixture.svg?branch=master

for python2.7, python3.5 and Django>=1.8

Create a fixture dict that just include some fields you concern, and we will help you to fill your fixture dict with some spam datas that
make your fixture dict to be a completely available django fixture that **you do not have to worry about any unqiue, unqie_together**

install: pip install django-easy-fixture

1. output a fixture dict
------------------------

**pk must be set by yourself**

in template.py

.. code-block:: python

   fixtures_template={'auth.User': [{'pk': 1}]}

then

.. code-block:: python

   from easy_fixture.easy_fixture import EasyFixture
   from template import fixtures_template

   ef = EasyFixture(fixtures_template)
   fixtures_dict = ef.output()

2. use as a django app command
------------------------------

2.1. create a simple fixture template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

in template.py

**pk must be set by yourself**

.. code-block:: python

   fixtures_template={'auth.User': [{'pk': 1}]}

2.2. in settings.py
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   INSTALLED_APPS = ('other apps',
                     'easy_fixture',
                     )

2.3. run command
~~~~~~~~~~~~~~~~
 
.. code-block:: python


   python manage.py make_fixture template > /path/to/fixture.json

3. use in test
--------------

.. code-block:: python

   from easy_fixture.easy_fixture import FixtureFileGen

   class MyCase(TestCase):
      fixtures = FixtureFileGen(['my.fixture.template.module'])
