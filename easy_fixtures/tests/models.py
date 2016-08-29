# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from django.db import models


class FixtureForeignModel(models.Model):
    postive_integer = models.PositiveIntegerField()
    postive_small_integer = models.PositiveSmallIntegerField()


class FixtureManyToManyModel(models.Model):
    biginteger_field = models.BigIntegerField()


class FixtureModel(models.Model):
    char_field = models.CharField(max_length=20)
    integer_field = models.IntegerField()
    dete_field = models.DateField()
    datetime_field = models.DateTimeField()
    foreign_field = models.ForeignKey(FixtureForeignModel)
    many_to_many = models.ManyToManyField(FixtureManyToManyModel)

    class Meta(object):
        unique_together = (('char_field', 'foreign_field'))
