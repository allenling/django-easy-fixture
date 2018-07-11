import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    sys.path.insert(0, os.path.dirname(__file__))

    from django.core.management import execute_from_command_line

    execute_from_command_line(['manage.py', 'test', 'testapp'])
#     execute_from_command_line(['manage.py', 'loaddata', 'fixture.json'])
    return


if __name__ == "__main__":
    main()
