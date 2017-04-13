from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
import requests
from simplejson import loads
from exchange.models import CurrencyRateIndex


class Command(BaseCommand):
    """ Rate update command """

    def handle(self, **options):
        if not getattr(settings, 'EXCHANGERATES_API', None):
            raise ImproperlyConfigured('No exchange rates service defined.')
        else:
            app_url = getattr(settings, 'EXCHANGERATES_API', False)
            response = requests.get(app_url)
            result = loads(response.content)
            crindex = CurrencyRateIndex.objects.all()
            if not crindex:
                if 'rates' in result:
                    for code in result['rates']:
                        rate_index = result['rates'][code]
                        if len(code) == 3 and type(rate_index) == float:
                            print "CREATE NEW %s : %s " % (code, rate_index)
                            CurrencyRateIndex.objects.create(
                                iso_code=code,
                                rate=rate_index,
                                tracked_by=app_url,
                            )
                        else:
                            print " ERROR Invalid data from API :%s " % app_url
                            print " %s : %s " % (code, rate_index)
                else:
                    print "ERROR Empty data from API :%s " % app_url
            else:
                for rate in crindex:
                    if rate.iso_code in result['rates']:
                        rate_index = result['rates'][rate.iso_code]
                        if type(rate_index) == float:
                            rate.rate = rate_index
                            rate.save()
                            print " UPDATE %s : %s " % (rate.iso_code, rate_index)
                        else:
                            print "ERROR"
                            print "---------------------------------------------------------"
                            print " Invalid data from API :%s " % app_url
                            print " %s : %s " % (code, rate_index)
                            print "---------------------------------------------------------"
                    else:
                        print "ERROR"
                        print "---------------------------------------------------------"
                        print "iso_code not found in result from API :%s " % app_url
                        print "iso_code search : %s " % rate.iso_code
                        print "CurrencyRateIndex id: %s " % rate.id
                        print "---------------------------------------------------------"
