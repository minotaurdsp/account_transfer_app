from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
import requests
from simplejson import loads
from api_key.models import APIKey


class Command(BaseCommand):
    def handle(self, **options):
        print "Create api key"
        apk = APIKey.objects.create(name="shared key",key="883c56997e38f96e25343eeecbdd40ab3f0f87d4")
        apk.save()
        print "shared key ",apk.key
