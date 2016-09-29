# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from django.db import models


class FixtureForeignModel(models.Model):
    postive_integer = models.PositiveIntegerField()
    postive_small_integer = models.PositiveSmallIntegerField()
    file_path_field = models.FilePathField()
    float_field = models.FloatField()
    ip = models.GenericIPAddressField()
    slug_field = models.SlugField()
    small_in = models.SmallIntegerField()
    text_field = models.TextField()
    time = models.TimeField()


class FixtureManyToManyModel(models.Model):
    biginteger_field = models.BigIntegerField()
    boolean_field = models.BooleanField()
    non_boolean_field = models.NullBooleanField()
    comma_sep_field = models.CommaSeparatedIntegerField(max_length=20, unique=True)
#     decimal_field = models.DecimalField()
    duration_field = models.DurationField()
    email = models.EmailField()


class FixtureModel(models.Model):
    unique_together_char_field_one = models.CharField(max_length=20, default='')
    unique_together_char_field_two = models.CharField(max_length=20, default='')
    char_field = models.CharField(max_length=20)
    integer_field = models.IntegerField()
    dete_field = models.DateField()
    datetime_field = models.DateTimeField()
    url = models.URLField()
    bin = models.BinaryField()
    uuid = models.UUIDField()
    foreign_field = models.ForeignKey(FixtureForeignModel)
    many_to_many = models.ManyToManyField(FixtureManyToManyModel)

    class Meta(object):
        unique_together = (('char_field', 'foreign_field'), ('unique_together_char_field_one', 'unique_together_char_field_two'))
