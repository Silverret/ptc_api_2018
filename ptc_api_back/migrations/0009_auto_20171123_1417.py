# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ptc_api_back', '0008_auto_20171123_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travelerprofile',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
