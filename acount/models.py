# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from exchange.utils import make_exchange
#from exchange.models import Currency

import numbers
from random import SystemRandom
from django.db import IntegrityError


def psrandgen():
    cryptogen = SystemRandom()
    return int("".join("{0}".format(cryptogen.randrange(9)) for i in range(8)))


def psrandgen_trans():
    cryptogen = SystemRandom()
    return int("".join("{0}".format(cryptogen.randrange(9)) for i in range(12)))


class InsufficientBalance(IntegrityError):
    """ Raised when a wallet has insufficient balance to
    run an operation.
    We're subclassing from :mod:`django.db.IntegrityError`
    so that it is automatically rolled-back during django's
    transaction lifecycle.
    """


class NegativeValue(IntegrityError):
    """ Raised when a wallet has insufficient balance to
    run an operation.
    We're subclassing from :mod:`django.db.IntegrityError`
    so that it is automatically rolled-back during django's
    transaction lifecycle.
    """


class Base(models.Model):
    created = models.DateTimeField(
        auto_now=False, auto_now_add=True, db_index=True, null=True)
    updated = models.DateTimeField(auto_now=True, db_index=True, null=True)

    class Meta:
        abstract = True


class Account(Base):
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    uid = models.IntegerField(
        unique=True,
        editable=False,
        default=psrandgen,
        verbose_name='Public identifier',
    )

    currency = models.ForeignKey(
        'exchange.Currency',
        related_name='accounts',
        verbose_name=_('Currency'),
    )

    current_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('Current balance'),
    )

    def positive_balance(self, value):
        if value < self.current_balance:
            return True
        else:
            return False

    def iso_code(self):
        return str(self.currency.iso_code)

    def deposit(self, value):
        """Deposits a value to the wallet.
        Also creates a new transaction with the deposit
        value.
        """
        try:
            account = Account.objects.filter(id=self.id).get()
            trans = Transaction(
                account=account,
                value=value,
                running_balance=self.current_balance + value,
                transaction_type='d',
                currency=self.currency)
            trans.save()
            account.current_balance += value
            account.save()
            return (trans.uid, trans.id, False, "")
        except:
            return (None, None, False, "deposit error")

    def withdraw(self, value):

        if not self.positive_balance(value):
            raise InsufficientBalance('Negative balance are not permitted.')

        try:
            account = Account.objects.filter(id=self.id).get()
            trans = Transaction(
                account=account,
                value=-value,
                running_balance=self.current_balance - value,
                transaction_type='w',
                currency=self.currency)
            trans.save()
            account.current_balance -= value
            account.save()

            return (trans.uid, trans.id, False, "")
        except:
            return (None, None, True, "withdraw error")

    def transfer(self, acount, value):
        """ 
        Internal transfers convert the transferred amount if the source 
        and destination accounts are denominated in different currencies.
        """
        if value.is_zero():
            raise NegativeValue('Negative value or value not defined.')

        if not self.iso_code() == acount.iso_code():
            ex_value = make_exchange(
                value, self.iso_code(), acount.iso_code())
        else:
            ex_value = value

        try:

            account_src = Account.objects.filter(id=self.id).get()
            account_dst = acount

            tr1 = self.withdraw(value)
            tr2 = acount.deposit(ex_value)

            trans_src = self.transaction_set.filter(id=tr1[1]).get()
            trans_dst = acount.transaction_set.filter(id=tr2[1]).get()

            trans_dst.parent = trans_src
            trans_src.parent = trans_dst

            trans_dst.save()
            trans_src.save()

            return (trans_src.uid, None, False, "")

        except Exception, e:
            print e
            return (None, None, True, "Server error ")

    def __str__(self):
        return " %s - %s " % (self.uid, self.iso_code())


class Transaction(models.Model):
    account = models.ForeignKey(Account)

    parent = models.ForeignKey(
        'Transaction',
        related_name='children',
        blank=True, null=True,
        verbose_name=_('Parent'),
    )

    uid = models.IntegerField(
        unique=True,
        editable=False,
        default=psrandgen_trans,
        verbose_name='Transaction identifier',
    )

    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('Value'),
    )
    running_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('Running balance'),
    )
    currency = models.ForeignKey(
        'exchange.Currency',
        related_name='transactions',
        verbose_name=_('Currency'),
    )

    TRANSACTION_TYPES = {
        'withdrawal': 'w',
        'deposit': 'd',
    }

    TRANSACTION_TYPE_CHOICES = [
        (TRANSACTION_TYPES['withdrawal'], 'withdrawal'),
        (TRANSACTION_TYPES['deposit'], 'deposit'),
    ]

    transaction_type = models.CharField(
        max_length=1,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name=_('Transaction type'),
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def status(self):
        if self.parent:
            return "Transfer"
        else:
            self.transaction_type
    status.short_description = 'trans status'

    def __str__(self):
        return "%s  %s  %s" % (
            self.transaction_type,
            self.value,
            self.currency
        )
