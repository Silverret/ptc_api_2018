# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-29 10:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Climate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('code', models.CharField(max_length=2)),
                ('advisory_state', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('malaria_presence', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CountryUnion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('t_visa_between_members', models.BooleanField()),
                ('common_visa', models.BooleanField()),
                ('countries', models.ManyToManyField(to='task_factory.Country')),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=63)),
                ('description', models.TextField()),
                ('countries', models.ManyToManyField(related_name='vaccines', to='task_factory.Country')),
            ],
        ),
        migrations.AddField(
            model_name='climate',
            name='country',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task_factory.Country'),
        ),
    ]
