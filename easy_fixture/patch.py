# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db.models import fields as django_fields
from django.utils import timezone


def get_field_max_plus_value(field_name, datas):
    return max([int(i[field_name]) for i in datas if field_name in i and str(i[field_name]).isdigit()] + [0]) + 1


def patch_CharField(model, data, datas, field_name, field, field_val, model_strings):
    return get_field_max_plus_value(field_name, datas)


def patch_PositiveIntegerField(model, data, datas, field_name, field, field_val, model_strings):
    return get_field_max_plus_value(field_name, datas)


def patch_PositiveSmallIntegerField(model, data, datas, field_name, field, field_val, model_strings):
    return get_field_max_plus_value(field_name, datas)


def patch_IntegerField(model, data, datas, field_name, field, field_val, model_strings):
    return get_field_max_plus_value(field_name, datas)


def patch_BigIntegerField(model, data, datas, field_name, field, field_val, model_strings):
    return get_field_max_plus_value(field_name, datas) % django_fields.BigIntegerField.MAX_BIGINT


def patch_DateTimeField(model, data, datas, field_name, field, field_val, model_strings):
    return timezone.now().strftime('%Y-%m-%d %H:%M:%S')


def patch_DateField(model, data, datas, field_name, field, field_val, model_strings):
    return timezone.now().date().strftime('%Y-%m-%d')


def patch_manytomany(model, data, datas, field_name, field, model_strings, fixtures):
    rel_model_string = '%s.%s' % (field.related_model._meta.app_label, field.related_model.__name__)
    rel_datas = []
    if rel_model_string not in fixtures:
        fixtures[rel_model_string] = []
    else:
        rel_datas = fixtures[rel_model_string]
    rel_exist_pks = [_['pk'] for _ in rel_datas]
    if field_name not in data:
        data[field_name] = [max(rel_exist_pks + [0]) + 1]
    assert data[field_name] is not None
    for rel_pk in data[field_name]:
        if rel_pk not in rel_exist_pks:
            fixtures[rel_model_string].append({'pk': rel_pk})
            if rel_model_string not in model_strings:
                model_strings.append(rel_model_string)


def patch_relation(model, data, datas, field_name, field, model_strings, fixtures):
    if field.many_to_many:
        patch_manytomany(model, data, datas, field_name, field, model_strings, fixtures)
        return
    rel_model_string = '%s.%s' % (field.related_model._meta.app_label, field.related_model.__name__)
    rel_datas = []
    if rel_model_string not in fixtures:
        fixtures[rel_model_string] = []
    else:
        rel_datas = fixtures[rel_model_string]
    rel_exist_pks = [_['pk'] for _ in rel_datas]
    if field_name not in data:
        data[field_name] = max(rel_exist_pks + [0]) + 1
    if data[field_name] is None:
        return
    if data[field_name] not in rel_exist_pks:
        fixtures[rel_model_string].append({'pk': data[field_name]})
        if rel_model_string not in model_strings:
            model_strings.append(rel_model_string)
