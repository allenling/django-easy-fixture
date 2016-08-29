# coding=utf-8
from __future__ import absolute_import

from setuptools import setup

version = "0.1.0"

from setuptools.command.test import test as test_command
import sys


class Tox(test_command):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        test_command.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        test_command.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

packages = ["easy_fixture",
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
      tests_require=['tox'],
      cmdclass={'test': Tox},
      install_requires=['Django >= 1.8'],
)
