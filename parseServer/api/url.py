from django.urls import path
from .views import *

urlpatterns = [
    path('car_ad_filter/', CarAdFilteredList.as_view(), name='car_ad_list'),
    path('car_ad/<int:ad_id>/', CarAdDetailView.as_view(), name='car_ad_detail'),
    path('area/', AreaList.as_view()),
    path('area/<str:name>/', AreaDetail.as_view()),
    path('region/', RegionList.as_view()),
    path('region/<str:name>/', RegionDetail.as_view()),
    path('country/', CountryList.as_view()),
    path('country/<str:name>/', CountryDetail.as_view()),
    path('brand/', BrandList.as_view(), name='brand_list'),
    path('brand/<str:brand>/', ModelsByBrand.as_view()),
    # path('models/', AllModelsByBrand.as_view(), name='all_models_by_brand'),
    path('currencies/', get_currency_list),
    path('<str:item>/', get_field_lists),

]
