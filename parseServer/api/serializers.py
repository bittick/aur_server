from rest_framework import serializers
from parseServer.models import *


class CarAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarAd
        fields = '__all__'


class CarAdFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarAd
        exclude = ('price_history', 'link')


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('name',)


class BrandSerializer(serializers.ModelSerializer):
    car_models = CarModelSerializer(many=True, read_only=True, source='carmodel_set')

    class Meta:
        model = Brand
        fields = ('name', 'car_models')


class EngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engine
        fields = '__all__'


class GearboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gearbox
        fields = '__all__'


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = '__all__'


class CarDriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarDrive
        fields = '__all__'


class CarConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCondition
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class AreaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['name']


class RegionSerializer(serializers.ModelSerializer):
    areas = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    regions = RegionSerializer(many=True, read_only=True)
    areas_without_region = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ['name', 'regions', 'areas_without_region']
