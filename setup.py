# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

from setuptools import setup

version = "0.0.1"

packages = [
            "easy_fixtures",
]

packages = [package.encode('ascii') for package in packages]  # package should be string type when using python<=2.7.6

setup(
      name="django-easy-fixtures",
      version=version,
      author="allenling",
      author_email="allenling3@gmail.com",
      url="git@github.com:allenling/django-easy-fixtures.git",
      classifiers=[
                    'Development Status :: 3 - Alpha',
                    'Environment :: Web Environment',
                    'Intended Audience :: Developers',
                    'Framework :: Django',
                    'Framework :: Django :: 1.8',
                    'License :: OSI Approved :: MIT License',
                    'Operating System :: OS Independent',
                    'Programming Language :: Python',
                    'Programming Language :: Python :: 2',
                    'Programming Language :: Python :: 2.7',
      ],
      license='MIT',
      packages=packages,
      include_package_data=True,
      install_requires=[],
)
