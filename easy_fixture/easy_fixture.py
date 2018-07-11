import base64
import uuid
import json
from collections import defaultdict

from django.db.models import fields as django_fields
from django.apps import apps
from django.utils import timezone

from easy_fixture.fixture_command import save_to_db

DATETIME_NOW = timezone.now()
DATE_NOW = DATETIME_NOW.date()


class WrapFileFixture:

    def __init__(self, data):
        self.data = data
        return

    def close(self):
        return


def get_next_datetime(delta_second):
    return str(DATETIME_NOW + timezone.timedelta(seconds=delta_second))


def get_next_date(delta_day):
    return str(DATE_NOW + timezone.timedelta(days=delta_day))


def field_to_bin(next_bin):
    return (base64.encodebytes(next_bin.encode())).decode()


def get_next_time(delta_second):
    return (DATETIME_NOW + timezone.timedelta(seconds=delta_second)).strftime('%H:%M:%S.%fZ')


def field_to_uuid(next_value):
    return uuid.uuid1().hex


def get_bool(next_value):
    return True if next_value % 2 == 0 else False


class EasyFixture:

    def __init__(self, fixtures):
        '''
        fixtures = {auth.User: {'pk1': {field1: 'field1', ...},
                                'pk2': {field2: 'field2', ...},
                                },
                    }
        '''
        self.fixtures = fixtures
        self.cached_app_model = {}
        self.module_model_data = {}
        return

    def get_model_necessary_fields(self, model_object):
        fields = {}
        fkey = {}
        many_key = {}
        uq_togethers = []
        model_meta = model_object._meta
        for uq in model_meta.unique_together:
            uq_togethers.extend(uq)
        uq_togethers = set(uq_togethers)
        for f in model_meta.get_fields():
            if isinstance(f, django_fields.reverse_related.ManyToOneRel):
                continue
            if isinstance(f, django_fields.reverse_related.ManyToManyRel):
                continue
            fname = f.name
            if f.remote_field is not None:
                frelated_model_meta = f.related_model._meta
                key = '%s.%s' % (frelated_model_meta.app_label, frelated_model_meta.model.__qualname__)
                if f.remote_field.__class__.__name__ == 'ManyToOneRel':
                    fkey[fname] = key
                elif f.remote_field.__class__.__name__ == 'ManyToManyRel':
                    many_key[fname] = key
                    continue
            if f.null is True and f.blank is True and fname not in uq_togethers:
                continue
            fields[fname] = f
        del fields['id']
        return {'fields': fields, 'fkey': fkey, 'many_key': many_key}

    def get_model_fs(self, module_model, cached_app_model):
        app_name, model_name = module_model.split('.')
        cached_app = cached_app_model.get(app_name, None)
        if cached_app is None:
            cached_app = {'app_config': apps.get_app_config(app_name)}
            cached_app_model[app_name] = cached_app
        model_fs = cached_app.get(model_name, None)
        if model_fs is None:
            model_object = cached_app['app_config'].get_model(model_name)
            model_fs = self.get_model_necessary_fields(model_object)
            cached_app[model_name] = model_fs
        return model_fs

    def get_model_data(self, module_model, model_value, model_fs, module_model_data):
        md = module_model_data.get(module_model, None)
        fields = model_fs['fields']
        many_key = model_fs['many_key']
        fkey = model_fs['fkey']
        if md is None:
            md = {i: 0 for i in fields}
            module_model_data[module_model] = md
        data = {**model_value}
        exist_field = set(data.keys())
        relations = []
        lefted_keys = set(fields.keys()) - exist_field
        for f in lefted_keys:
            next_value = md[f] + 1
            ffield = fields[f]
            md[f] = next_value
            if ffield.__class__.__qualname__ == 'DateTimeField':
                data[f] = get_next_datetime(next_value)
            elif ffield.__class__.__qualname__ == 'DateField':
                data[f] = get_next_date(next_value)
            elif ffield.__class__.__qualname__ == 'BinaryField':
                data[f] = field_to_bin(str(next_value))
            elif ffield.__class__.__qualname__ == 'TimeField':
                data[f] = get_next_time(next_value)
            elif ffield.__class__.__qualname__ == 'UUIDField':
                data[f] = field_to_uuid(next_value)
            elif ffield.__class__.__qualname__ == 'BooleanField':
                data[f] = get_bool(next_value)
            else:
                data[f] = str(next_value)
        data_keys = set(data.keys())
        for f in data_keys & set(fkey.keys()):
            fkey_name = fkey[f]
            relations.append([fkey_name, data[f]])
        for f in data_keys & set(many_key.keys()):
            mf_name = many_key[f]
            for mf_pk in data[f]:
                relations.append([mf_name, mf_pk])
        if 'pk' in data:
            del data['pk']
        return data, relations

    def get_fixture_data(self):
        fixture_data = defaultdict(dict)
        relation_models = []
        cached_app_model = self.cached_app_model
        module_model_data = self.module_model_data
        fixtures = self.fixtures
        for module_model, model_values in fixtures.items():
            model_fs = self.get_model_fs(module_model, cached_app_model)
            for model_value in model_values:
                pk = model_value.pop('pk')
                data, releations = self.get_model_data(module_model, model_value, model_fs, module_model_data)
                fixture_data[module_model][pk] = {'pk': pk, 'model': module_model.lower(), 'fields': data}
                if releations is not None:
                    relation_models.extend(releations)
        # fill foreign key, many to many
        while relation_models:
            module_model, pk = relation_models.pop()
            if pk in fixture_data[module_model]:
                continue
            model_fs = self.get_model_fs(module_model, cached_app_model)
            data, releations = self.get_model_data(module_model, {'pk': pk}, model_fs, module_model_data)
            fixture_data[module_model][pk] = {'pk': pk, 'model': module_model.lower(), 'fields': data}
            if releations is not None:
                relation_models.extend(releations)
        json_data = []
        for i in fixture_data:
            module_data = fixture_data[i]
            for _, value in module_data.items():
                json_data.append(value)
        return json_data

    def save(self):
        '''
        save data into db
        '''
        data = self.get_fixture_data()
        wrap_file_fixture = WrapFileFixture(data)
        save_to_db(wrap_file_fixture)
        return

    def save_file(self, file_path='fixture.json'):
        '''
        save data into file
        '''
        data = self.get_fixture_data()
        with open(file_path, 'w') as f:
            json.dump(data, f)
        return


# class FixtureFileGen:
# 
#     def __init__(self, templates, file_path='fixtures'):
#         self.templates = templates
#         self.file_path = file_path
#         self.index = 0
#         return
# 
#     def next(self):
#         if self.index < len(self.templates):
#             template = self.templates[self.index]
#             tem = importlib.import_module(template)
#             ef = EasyFixture(tem.fixtures_template)
#             fixture_path = os.path.join(self.file_path, os.path.basename(tem.__file__).split('.')[0]) + '.json'
#             with open(fixture_path, 'w') as f:
#                 f.write(ef.output())
#             self.index += 1
#             return fixture_path
#         else:
#             raise StopIteration
# 
#     def __iter__(self):
#         return self
