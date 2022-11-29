
from operator import mod
from pydoc import describe
from unittest.util import _MAX_LENGTH
from django.db import models
from sqlalchemy import false, null, true


class Course(models.Model):

    name = models.CharField(max_length=30, null=False)
    slug = models.CharField(max_length=50, null=False, unique=True)
    description = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False, default=0)
    active = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to="files/thumbnail")
    date = models.DateTimeField(auto_now_add=True)
    resource = models.FileField(upload_to="files/resources")
    length = models.IntegerField(null=False)

    def __str__(self):
        return self.name


class CourseProperty(models.Model):
    description = models.CharField(max_length=20, null=False)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)

# so that table for this not created in database.
    class Meta:
        abstract = True


class Tag(CourseProperty):
    pass


class Prerequisite(CourseProperty):
    pass


class Learning(CourseProperty):
    pass


class CouponCode(models.Model):
    code = models.CharField(max_length=10)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='coupons')
    discount=models.IntegerField(default=0)
