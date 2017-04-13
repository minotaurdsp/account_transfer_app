# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-10 19:34
from __future__ import unicode_literals

import acount.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('uid', models.IntegerField(default=acount.models.psrandgen, editable=False, unique=True, verbose_name='Public identifier')),
                ('current_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Current balance')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='exchange.Currency', verbose_name='Currency')),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(default=acount.models.psrandgen, editable=False, unique=True, verbose_name='Transaction identifier')),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Value')),
                ('running_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Running balance')),
                ('transaction_type', models.CharField(choices=[('w', 'withdrawal'), ('d', 'deposit')], max_length=1, verbose_name='Transaction type')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acount.Account')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='exchange.Currency', verbose_name='Currency')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='acount.Transaction', verbose_name='Parent')),
            ],
        ),
    ]
