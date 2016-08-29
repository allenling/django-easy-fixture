# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from collections import defaultdict
import os
import importlib

from django.db.models import fields as django_fields
from django.apps import apps
from django.utils import timezone


class EasyFixture(object):

    def __init__(self, fixtures):
        self.initial_fixtures(fixtures)
        self.finish_map = defaultdict(list)
        self.model_field_val = {}
        self.models = {}

    def initial_fixtures(self, fixtures):
        self.fixtures = {}
        for fixture in fixtures:
            self.fixtures[fixture] = []
            for data in fixtures[fixture]:
                tmp = {}
                tmp.update(data)
                self.fixtures[fixture].append(tmp)

    def get_model(self, model_string):
        if model_string not in self.models:
            app_name, model_name = model_string.split('.')
            app_config = apps.get_app_config(app_name)
            self.models[model_string] = app_config.get_model(model_name)
        return self.models[model_string]

    def get_model_field_val(self, model_string):
        model = self.get_model(model_string)
        if model_string not in self.model_field_val:
            field_val = {}
            for f in [f for f in model._meta.fields if f.name != 'id']:
                if f.null is False and f.blank is False and f.default is django_fields.NOT_PROVIDED or \
                        isinstance(f, (django_fields.DateField, django_fields.DateTimeField)):
                    field_val[f.name] = f
            self.model_field_val[model_string] = field_val
        return self.model_field_val[model_string]

    def patch_CharField(self, model, data, datas, field_name, field, field_val, model_strings):
        return str(max([int(i[field_name]) for i in datas if field_name in i and i[field_name].isdigit()] + [0]) + 1)

    def patch_PositiveIntegerField(self, model, data, datas, field_name, field, field_val, model_strings):
        return max([int(i[field_name]) for i in datas if field_name in i and i[field_name]] + [0]) + 1

    def patch_PositiveSmallIntegerField(self, model, data, datas, field_name, field, field_val, model_strings):
        return max([int(i[field_name]) for i in datas if field_name in i and i[field_name]] + [0]) + 1

    def patch_IntegerField(self, model, data, datas, field_name, field, field_val, model_strings):
        return max([int(i[field_name]) for i in datas if field_name in i and i[field_name]] + [0]) + 1

    def patch_BigIntegerField(self, model, data, datas, field_name, field, field_val, model_strings):
        return (max([int(i[field_name]) for i in datas if field_name in i and i[field_name]] + [0]) + 1) % django_fields.BigIntegerField.MAX_BIGINT

    def patch_DateTimeField(self, model, data, datas, field_name, field, field_val, model_strings):
        return timezone.now().strftime('%Y-%m-%d %H:%M:%S')

    def patch_DateField(self, model, data, datas, field_name, field, field_val, model_strings):
        return timezone.now().date().strftime('%Y-%m-%d')

    def patch_field(self, model, data, datas, field_name, field, field_val, model_strings):
        if field.choices:
            data[field_name] = field.choices[0][0]
            return
        if field.is_relation:
            if field.many_to_many:
                self.patch_manytomany(model, data, datas, field_name, field, model_strings)
            else:
                self.patch_relation(model, data, datas, field_name, field, model_strings)
        else:
            method_name = getattr(self, 'patch_%s' % type(field).__name__, None)
            if method_name is None:
                raise StandardError('do not support this %s field type yet' % type(field).__name__)
            data[field_name] = method_name(model, data, datas, field_name, field, field_val, model_strings)

    def patch_manytomany(self, model, data, datas, field_name, field, model_strings):
        rel_model_string = '%s.%s' % (field.related_model._meta.app_label, field.related_model.__name__)
        rel_datas = []
        if rel_model_string not in self.fixtures:
            self.fixtures[rel_model_string] = []
        else:
            rel_datas = self.fixtures[rel_model_string]
        rel_exist_pks = [_['pk'] for _ in rel_datas]
        if field_name not in data:
            data[field_name] = [max(rel_exist_pks + [0]) + 1]
        assert data[field_name] is not None
        for rel_pk in data[field_name]:
            if rel_pk not in rel_exist_pks:
                self.fixtures[rel_model_string].append({'pk': rel_pk})
                if rel_model_string not in model_strings:
                    model_strings.append(rel_model_string)

    def patch_relation(self, model, data, datas, field_name, field, model_strings):
        rel_model_string = '%s.%s' % (field.related_model._meta.app_label, field.related_model.__name__)
        rel_datas = []
        if rel_model_string not in self.fixtures:
            self.fixtures[rel_model_string] = []
        else:
            rel_datas = self.fixtures[rel_model_string]
        rel_exist_pks = [_['pk'] for _ in rel_datas]
        if field_name not in data:
            data[field_name] = max(rel_exist_pks + [0]) + 1
        if data[field_name] is None:
            return
        if data[field_name] not in rel_exist_pks:
            self.fixtures[rel_model_string].append({'pk': data[field_name]})
            if rel_model_string not in model_strings:
                model_strings.append(rel_model_string)

    def clean_model_data(self, model_string, model, datas, field_val, model_strings):
        for data in datas:
            assert 'pk' in data
            if data['pk'] in self.finish_map[model_string]:
                continue
            for field_name in field_val:
                if field_name not in data:
                    self.patch_field(model, data, datas, field_name, model._meta.get_field(field_name), field_val, model_strings)
            for field_name in data:
                if field_name == 'pk':
                    continue
                field = model._meta.get_field(field_name)
                if field.is_relation and field_name not in field_val:
                    self.patch_field(model, data, datas, field_name, field, field_val, model_strings)
            self.finish_map[model_string].append(data['pk'])

    def return_complete_fixtures(self):
        fixtures_data = []
        for model_string in self.fixtures:
            datas = self.fixtures[model_string]
            app_name, model_name = model_string.split('.')
            model_str = '%s.%s' % (app_name, model_name.lower())
            for data in datas:
                pk = data.pop('pk')
                fixtures_data.append({'model': model_str, 'pk': pk, 'fields': data})
        return fixtures_data

    def output(self):
        model_strings = list(self.fixtures.keys())
        while model_strings:
            model_string = model_strings.pop()
            datas = self.fixtures.get(model_string, [])
            model = self.get_model(model_string)
            field_val = self.get_model_field_val(model_string)
            self.clean_model_data(model_string, model, datas, field_val, model_strings)
        return self.return_complete_fixtures()


class FixtureFileGen(object):

    def __init__(self, templates, file_path='fixtures'):
        self.templates = templates
        self.file_path = file_path
        self.index = 0

    def next(self):
        if self.index < len(self.templates):
            template = self.templates[self.index]
            tem = importlib.import_module(template)
            ef = EasyFixture(tem.fixtures_template)
            fixture_path = os.path.join(self.file_path, os.path.basename(tem.__file__).split('.')[0]) + '.json'
            with open(fixture_path, 'w') as f:
                f.write(ef.output())
            self.index += 1
            return fixture_path
        else:
            raise StopIteration

    def __iter__(self):
        return self
