# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-10 19:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_code', models.CharField(max_length=3, unique=True, verbose_name='ISO-code')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
            ],
            options={
                'ordering': ['iso_code'],
            },
        ),
        migrations.CreateModel(
            name='CurrencyRateIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_code', models.CharField(max_length=3, unique=True, verbose_name='ISO-code')),
                ('rate', models.DecimalField(decimal_places=8, max_digits=17)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('tracked_by', models.CharField(default='Add your email', max_length=512, verbose_name='Tracked by')),
            ],
            options={
                'ordering': ['iso_code'],
            },
        ),
    ]
