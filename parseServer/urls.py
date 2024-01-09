from django.urls import path, include

urlpatterns = [
    path('api/', include('parseServer.api.url'))
    # path('api/kufar_ads', kufar_ads_process),
    # path('api/lalafo_ads', lalafo_ads_process)
    ]
