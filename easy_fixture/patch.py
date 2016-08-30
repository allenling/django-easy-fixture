# coding=utf-8
'''
any CharField or CharField subclass and any IntegerField or IntegerField subclass
and FloatField or FloatField subclass could be set to max(value) + 1

field validator only be call when use a form

when load data, only to_python method should be concern

'''
from __future__ import unicode_literals
from __future__ import absolute_import
import uuid
import base64

from django.db.models import fields as django_fields
from django.utils import timezone

base64encode = getattr(base64, 'encodebytes', base64.encodestring)
base64decode = getattr(base64, 'decodebytes', base64.decodestring)


def filter_float(value):
    try:
        float(value)
    except:
        return False
    else:
        return True


def get_field_max_plus_value(field_name, datas):
    return max([int(i[field_name]) for i in datas if field_name in i and str(i[field_name]).isdigit()] + [0]) + 1


def patch_BooleanField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = True
    return


def patch_CharField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = get_field_max_plus_value(field_name, datas)
    return


def patch_CommaSeparatedIntegerField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = get_field_max_plus_value(field_name, datas)
    return


def patch_DateField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = timezone.now().date().strftime('%Y-%m-%d')
    return


def patch_DateTimeField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    return


def patch_DecimalField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = get_field_max_plus_value(field_name, datas)
    return


def patch_DurationField(model, data, datas, field_name, field, field_val, model_strings):
    field_datas = [django_fields.parse_duration(i[field_name]).total_seconds() for i in datas if field_name in i]
    data[field_name] = str(max(field_datas + [0]) + 1)
    return


def patch_EmailField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = get_field_max_plus_value(field_name, datas)
    return


def patch_FilePathField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = str(get_field_max_plus_value(field_name, datas))
    return


def patch_FloatField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = max([float(i[field_name]) for i in datas if field_name in i and filter_float(i[field_name])] + [0]) + 1.0
    return


def patch_IntegerField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = get_field_max_plus_value(field_name, datas)
    return


def patch_BigIntegerField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = get_field_max_plus_value(field_name, datas) % django_fields.BigIntegerField.MAX_BIGINT
    return


def patch_GenericIPAddressField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = str(get_field_max_plus_value(field_name, datas))
    return


# for Django<=1.8
def patch_IPAddressField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = patch_GenericIPAddressField(model, data, datas, field_name, field, field_val, model_strings)
    return


def patch_NullBooleanField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = None
    return


def patch_PositiveIntegerField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = get_field_max_plus_value(field_name, datas)
    return


def patch_PositiveSmallIntegerField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = get_field_max_plus_value(field_name, datas)
    return


def patch_SlugField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = get_field_max_plus_value(field_name, datas)
    return


def patch_SmallIntegerField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = get_field_max_plus_value(field_name, datas)
    return


def patch_TextField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = str(get_field_max_plus_value(field_name, datas))
    return


def patch_TimeField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = timezone.now().strftime('%H:%M:%S')
    return


def patch_URLField(model, data, datas, field_name, field, field_val, model_strings):
    data[field_name] = get_field_max_plus_value(field_name, datas)
    return


def patch_BinaryField(model, data, datas, field_name, field, field_val, model_strings):
    field_datas = [base64decode(bytes(i[field_name].encode('utf-8'))) for i in datas if field_name in i]
    max_value = str((max([int(i) for i in field_datas if i.isdigit()] + [0]) + 1)).encode('utf-8')
    b64 = base64encode(bytes(max_value))
    data[field_name] = b64.decode('utf-8').replace('\n', '')
    return


def patch_UUIDField(model, data, datas, field_name, field, field_val, model_strings):
    # make a UUID based on the host ID and current time
    data[field_name] = uuid.uuid1().hex
    return


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
    return


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
    return
