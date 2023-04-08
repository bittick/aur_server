from django.contrib import admin
from .models import *


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')


@admin.register(Aggregator)
class AggregatorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'region')


@admin.register(CarCondition)
class CarConditionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(CarDrive)
class CarDriveAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Gearbox)
class GearboxAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(CarAd)
class CarAdAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model', 'price', 'aggregator',)
    readonly_fields = ('create_date', 'edit_date')
    list_filter = ('aggregator', 'brand', 'condition')
