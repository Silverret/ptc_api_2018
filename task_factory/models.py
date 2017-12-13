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
