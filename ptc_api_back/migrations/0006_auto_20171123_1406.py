# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 13:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ptc_api_back', '0005_auto_20171123_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travelerprofile',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='travelerprofile',
            name='birth_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='travelerprofile',
            name='nationalities',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='travelerprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='travelerprofile',
            name='residence_country',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='travelerprofile',
            name='traveler',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='travelerprofile',
            name='vaccines',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='travelerprofile',
            name='visas',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='travelerprofile',
            name='visited_countries',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
