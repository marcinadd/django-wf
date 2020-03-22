from django.db import models


class Class(models.Model):
    name = models.CharField(max_length=5)
    year = models.SmallIntegerField()

    def __str__(self):
        return self.name + " " + str(self.year)


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    clazz = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + str(self.clazz)


class Sport(models.Model):
    class Unit(models.TextChoices):
        KILOGRAM = 'kg', 'kilogram'
        METER = 'm', 'metr'
        SECOND = 's', 'sekunda'
        NONE = '', ''

    name = models.CharField(max_length=40)
    unit = models.CharField(max_length=2, choices=Unit.choices, default=Unit.NONE)
    more_better = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Result(models.Model):
    value = models.DecimalField(max_digits=4, decimal_places=2)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.value) + " " + self.sport.unit + " " + str(self.sport) + " " + str(self.group) + " " + str(
            self.student)
