from django.urls import path, include

urlpatterns = [
    path('api/', include('parseServer.api_v1.url'))
    # path('api_v1/kufar_ads', kufar_ads_process),
    # path('api_v1/lalafo_ads', lalafo_ads_process)
    ]
