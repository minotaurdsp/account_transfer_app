# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-11 21:30
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('key', models.CharField(max_length=40, unique=True)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name_plural': 'API Keys',
            },
        ),
    ]
