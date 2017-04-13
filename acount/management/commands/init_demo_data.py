from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from acount.models import Account , Transaction
from exchange.models import Currency

class Command(BaseCommand):
    def handle(self, **options):
        if not getattr(settings, 'CURRENCY_LIST', None):
            raise ImproperlyConfigured('No demo Currency list defined in settings')
        else:
            currency_list = getattr(settings, 'CURRENCY_LIST', False)
            for currency in currency_list:
                if not Currency.objects.filter(iso_code=currency).exists():
                    Currency.objects.create(iso_code=currency)
                if not Account.objects.filter(currency__iso_code=currency).exists():
                    Account.objects.create(
                    currency=Currency.objects.filter(iso_code=currency).get(),
                    current_balance=0
                )
           






