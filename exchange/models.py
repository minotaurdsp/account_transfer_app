# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Currency(models.Model):
    iso_code = models.CharField(
        verbose_name=_('ISO-code'),
        max_length=3,
        unique=True,
    )

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=50,
    )

    class Meta:
        ordering = ['iso_code']

    def save(self, *args, **kwargs):
        self.iso_code = self.iso_code.upper()
        super(Currency, self).save(*args, **kwargs)

    def __str__(self):
        return self.iso_code


class CurrencyRateIndex(models.Model):
    iso_code = models.CharField(
        verbose_name=_('ISO-code'),
        max_length=3,
        unique=True,
    )
    rate = models.DecimalField(max_digits=17, decimal_places=8)
    date = models.DateTimeField(
        verbose_name=_('Date'),
        auto_now_add=True,
    )
    tracked_by = models.CharField(
        max_length=512,
        verbose_name=_('Tracked by'),
        default=_('Add your email'),
    )
    class Meta:
        ordering = ['iso_code']

    def save(self, *args, **kwargs):
        self.iso_code = self.iso_code.upper()
        super(CurrencyRateIndex, self).save(*args, **kwargs)

    def __str__(self):
        return self.iso_code

