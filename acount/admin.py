# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Account, Transaction




class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0
    readonly_fields = ('currency', 'transaction_type',
                       'value', 'running_balance', 'uid')
    raw_id_fields = ['parent', 'account']


class AccountAdmin(admin.ModelAdmin):
    inlines = [
        TransactionInline,
    ]
    readonly_fields = ('uid',)
    list_display = ('currency', 'current_balance', 'uid')


class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('currency', 'transaction_type',
                       'value', 'running_balance', 'uid')
    raw_id_fields = ['parent', 'account']


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
