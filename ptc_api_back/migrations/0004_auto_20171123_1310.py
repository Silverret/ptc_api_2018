# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 12:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ptc_api_back', '0003_auto_20171123_1245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='travelerprofile',
            old_name='user',
            new_name='traveler',
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='user',
            new_name='traveler',
        ),
    ]
