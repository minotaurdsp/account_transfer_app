from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from acount import views

urlpatterns = [
    url(r'^accounts',views.accounts),
    url(r'^transactions',views.transactions),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls)
]
