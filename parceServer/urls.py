from django.urls import path
from .api.workers_api import *

urlpatterns = [
    path('api/kufar_ads', kufar_ads_process),
    # path('api/lalafo_ads', lalafo_ads_process)
    ]
