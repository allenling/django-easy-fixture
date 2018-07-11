from django.db import models


class TestAbstractModel(models.Model):
    postive_integer = models.PositiveIntegerField()
    postive_small_integer = models.PositiveSmallIntegerField()
    file_path_field = models.FilePathField()
    float_field = models.FloatField()
    ip = models.GenericIPAddressField()
    slug_field = models.SlugField()
    small_integer = models.SmallIntegerField()
    text_field = models.TextField()
    time_field = models.TimeField()
    biginteger_field = models.BigIntegerField()
    boolean_field = models.BooleanField()
    non_boolean_field = models.NullBooleanField()
#     decimal_field = models.DecimalField()
    duration_field = models.DurationField()
    email_field = models.EmailField()
    char_field = models.CharField(max_length=20)
    integer_field = models.IntegerField()
    dete_field = models.DateField()
    datetime_field = models.DateTimeField()
    url = models.URLField()
    bin = models.BinaryField()
    uuid = models.UUIDField()

    default_field = models.CharField(max_length=20, default='')
    unique_field = models.CharField(max_length=20)
    unique_together_field_a = models.CharField(max_length=20)
    unique_together_field_b = models.CharField(max_length=20)

    class Meta:
        abstract = True


class OtherModel(TestAbstractModel):
    pass


class FixtureForeignModel(TestAbstractModel):

    foreign_field = models.ForeignKey(OtherModel, on_delete=models.CASCADE)

    class Meta(object):
        unique_together = (('char_field', ), ('unique_together_field_a', 'unique_together_field_b'))


class FixtureManyToManyModel(TestAbstractModel):

    class Meta(object):
        unique_together = (('float_field', ), ('integer_field', ), ('unique_together_field_a', 'unique_together_field_b'))


class FixtureModel(TestAbstractModel):

    foreign_field = models.ForeignKey(FixtureForeignModel, on_delete=models.CASCADE)
    many_to_many = models.ManyToManyField(FixtureManyToManyModel)

    class Meta(object):
        unique_together = (('char_field', 'foreign_field'), ('unique_together_field_a', 'unique_together_field_b'))
