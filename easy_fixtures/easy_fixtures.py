# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
import importlib
from collections import defaultdict
import json

from django.db.models import fields as django_fields
from django.utils import timezone


class EasyFixtures(object):

    def __init__(self, fixtures):
        self.fixtures = {}
        for fixture in fixtures:
            self.fixtures[fixture] = [i for i in fixtures[fixture]]
        self.finish_map = defaultdict(list)
        self.model_field_val = {}
        self.models = {}

    def get_model(self, model_string):
        if model_string not in self.models:
            app, model_name = model_string.split('.')
            app_module = importlib.import_module(app + '.models')
            self.models[model_string] = getattr(app_module, model_name)
        return self.models[model_string]

    def get_model_field_val(self, model_string):
        model = self.get_model(model_string)
        if model_string not in self.model_field_val:
            field_val = {'requires': {}, 'unique': {}, 'unique_together': []}
            field_val['unique_together'].extend(model._meta.unique_together)
            for f in model._meta.fields:
                if f.name == 'id':
                    continue
                if f.null is False and f.blank is False and f.default is django_fields.NOT_PROVIDED or \
                        isinstance(f, (django_fields.DateField, django_fields.DateTimeField)):
                    field_val['requires'][f.name] = f
                if f.unique:
                    field_val[f.name] = f
            self.model_field_val[model_string] = field_val
        return self.model_field_val[model_string]

    def patch_CharField(self, model, data, datas, field_name, field, field_val, model_strings):
        return str(max([int(i[field_name]) for i in datas if field_name in i and i[field_name].isdigit()] + [0]) + 1)

    def patch_PositiveIntegerField(self, model, data, datas, field_name, field, field_val, model_strings):
        return max([int(i[field_name]) for i in datas if field_name in i and i[field_name]] + [0]) + 1

    def patch_IntegerField(self, model, data, datas, field_name, field, field_val, model_strings):
        return max([int(i[field_name]) for i in datas if field_name in i and i[field_name]] + [0]) + 1

    def patch_DateTimeField(self, model, data, datas, field_name, field, field_val, model_strings):
        return timezone.now().strftime('%Y-%m-%d %H:%M:%S')

    def patch_DateField(self, model, data, datas, field_name, field, field_val, model_strings):
        return timezone.now().date().strftime('%Y-%m-%d %H:%M:%S')

    def patch_field(self, model, data, datas, field_name, field, field_val, model_strings):
        if field.is_relation:
            self.patch_relation(model, data, datas, field_name, field, model_strings)
        else:
            method_name = getattr(self, 'patch_%s' % type(field).__name__, None)
            if method_name is None:
                print type(field).__name__
                raise StandardError('do not support this field yet')
            data[field_name] = method_name(model, data, datas, field_name, field, field_val, model_strings)

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
            if data['pk'] in self.finish_map[model_string]:
                continue
            for field_name in field_val['requires']:
                if field_name not in data:
                    self.patch_field(model, data, datas, field_name, model._meta.get_field(field_name), field_val, model_strings)
            for field_name in data:
                if field_name == 'pk':
                    continue
                field = model._meta.get_field(field_name)
                if field.is_relation:
                    self.patch_relation(model, data, datas, field_name, field, model_strings)
            self.finish_map[model_string].append(data['pk'])

    def write(self, wirteable):
        fixtures_data = []
        for model_string, datas in self.fixtures.iteritems():
            app_label, model_name = model_string.split('.')
            model_str = '%s.%s' % (app_label, model_name.lower())
            for data in datas:
                pk = data.pop('pk')
                fixtures_data.append({'model': model_str, 'pk': pk, 'fields': data})
        json.dump(fixtures_data, wirteable)

    def output(self, wirteable):
        model_strings = self.fixtures.keys()
        while model_strings:
            model_string = model_strings.pop()
            datas = self.fixtures.get(model_string, [])
            data_fields = datas[0].keys() if datas else []
            model = self.get_model(model_string)
            if data_fields:
                assert 'pk' in data_fields
            field_val = self.get_model_field_val(model_string)
            self.clean_model_data(model_string, model, datas, field_val, model_strings)
        self.write(wirteable)
