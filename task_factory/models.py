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
    advisory_state = models.PositiveSmallIntegerField(null=True, blank=True)
    malaria_presence = models.BooleanField(default=False)

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

class Vaccine(models.Model):
    """
    A Vaccine from Tugo API (see: URL in settings.py)
    """
    category = models.CharField(max_length=63)
    description = models.TextField()
    countries = models.ManyToManyField(Country, related_name='vaccines')

    def __str__(self):
        return self.category

class Climate(models.Model):
    """
    Climate info from Tugo API (see: URL in settings.py)
    """
    description = models.TextField()
    country = models.OneToOneField(Country, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.country.name
