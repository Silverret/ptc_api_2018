# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 09:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nationalities', models.CharField(blank=True, max_length=255)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('visas', models.CharField(blank=True, max_length=255)),
                ('address', models.CharField(blank=True, default='', max_length=255)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('visited_countries', models.CharField(blank=True, max_length=255)),
                ('vaccines', models.CharField(blank=True, max_length=255)),
                ('residence_country', models.CharField(blank=True, max_length=255)),
                ('traveler', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_country', models.CharField(max_length=255)),
                ('departure_airport', models.CharField(max_length=255)),
                ('departure_date_time', models.DateTimeField()),
                ('arrival_country', models.CharField(max_length=255)),
                ('arrival_airport', models.CharField(max_length=255)),
                ('arrival_date_time', models.DateTimeField()),
                ('order', models.IntegerField()),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('comments', models.TextField(blank=True, null=True)),
                ('auto', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_country', models.CharField(max_length=255)),
                ('departure_airport', models.CharField(max_length=255)),
                ('departure_date_time', models.DateTimeField()),
                ('arrival_country', models.CharField(max_length=255)),
                ('arrival_airport', models.CharField(max_length=255)),
                ('arrival_date_time', models.DateTimeField()),
                ('return_date_time', models.DateTimeField(blank=True, null=True)),
                ('traveler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='ptc_api_back.Trip'),
        ),
        migrations.AddField(
            model_name='segment',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='segments', to='ptc_api_back.Trip'),
        ),
    ]
