from rest_framework import permissions
from api_key.models import APIKey


class HasAPIAccess(permissions.BasePermission):
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view):
        print "TEST ACCESS ",request.META
        api_key = request.META.get('HTTP_API_KEY', '')
        print "api_key ",api_key
        print APIKey.objects.filter(key=api_key).exists()
        return APIKey.objects.filter(key=api_key).exists()