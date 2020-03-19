from django.db import models


class Class(models.Model):
    name = models.CharField(max_length=5)
    year = models.SmallIntegerField()

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    clazz = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)

class Sport(models.Model):
    class Unit(models.TextChoices):
        KILOGRAM = 'kg', ('kilogram')
        METER = 'm', ('metr')
        SECOND = 's', ('sekunda')
        NONE = '', ('')
    name = models.CharField(max_length=40)
    unit = models.CharField(max_length=2, choices=Unit.choices, default=Unit.NONE)
    more_better = models.BooleanField()

class Result(models.Model):
    value = models.DecimalField(max_digits=4, decimal_places=2)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()