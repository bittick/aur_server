from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')


@admin.register(Aggregator)
class AggregatorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(CarAd)
class CarAdAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model', 'price')
    readonly_fields = ('create_date', 'edit_date')
    list_filter = ('aggregator', 'brand')
