from django.conf.urls import url
from rest_framework import routers
from .views import CbbcViewSet

urlpatterns = [url(r'^api/cbbc/daily_summary/$', CbbcViewSet.as_view(), name='cbbc')]