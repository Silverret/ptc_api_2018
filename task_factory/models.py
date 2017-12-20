"""
The models used in the TaskFactory :
Country
"""
from django.db import models


class Country(models.Model):
    """
    A really simplist country model.
    """
    name = models.CharField(max_length=63)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class CountryUnion(models.Model):
    """
    A Union of Country has specific visa policies
    """
    name = models.CharField(max_length=63)
    t_visa_between_members = models.BooleanField()
    common_visa = models.BooleanField()
    countries = models.ManyToManyField(Country)

    def __str__(self):
        return self.name
