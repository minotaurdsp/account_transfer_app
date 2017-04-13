from models import CurrencyRateIndex

from django.utils.translation import ugettext_lazy as _


def make_exchange(amount, from_currency, to_currency):
    from_rate = CurrencyRateIndex.objects.filter(iso_code=from_currency)
    to_rate = CurrencyRateIndex.objects.filter(iso_code=to_currency)
    if not from_rate.exists() and not from_currency == 'USD':
        print "ERROR !!"
        print "Can not make exchange becouse CurrencyRateIndex not exist iso_code : %s " % from_currency
        return False
    elif not to_rate.exists() and not to_currency == 'USD':
        print "ERROR !!"
        print "Can not make exchange becouse CurrencyRateIndex not exist iso_code : %s " % to_currency
        return False
    else:
        if from_currency == 'USD':
            output_currency_to_usd = 1
        else:
            output_currency_to_usd = 1 / from_rate.get().rate
        if to_currency == 'USD':
            usd_to_input_currency = 1
        else:
            usd_to_input_currency = to_rate.get().rate
        result = amount * (output_currency_to_usd * usd_to_input_currency)
        return result
