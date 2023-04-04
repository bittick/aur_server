from django.urls import path
from .views import CarAdFilteredList, CarAdDetailView, BrandList, AllModelsByBrand, ModelsByBrand, get_field_lists

urlpatterns = [
    path('car_filter/', CarAdFilteredList.as_view(), name='car_ad_list'),
    path('car_ad/<int:ad_id>/', CarAdDetailView.as_view(), name='car_ad_detail'),
    path('brand/', BrandList.as_view(), name='brand_list'),
    path('brand/<str:brand>/', ModelsByBrand.as_view()),
    path('models/', AllModelsByBrand.as_view(), name='all_models_by_brand'),
    path('<str:item>/', get_field_lists),

]
