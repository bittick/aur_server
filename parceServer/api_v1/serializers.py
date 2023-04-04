from rest_framework import serializers
import parceServer.models


class CarAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = parceServer.models.CarAd
        fields = '__all__'


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = parceServer.models.CarModel
        fields = ('name',)


class BrandSerializer(serializers.ModelSerializer):
    car_models = CarModelSerializer(many=True, read_only=True, source='carmodel_set')

    class Meta:
        model = parceServer.models.Brand
        fields = ('name', 'car_models')


class EngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = parceServer.models.Engine
        fields = '__all__'


class GearboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = parceServer.models.Gearbox
        fields = '__all__'


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = parceServer.models.CarType
        fields = '__all__'


class CarDriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = parceServer.models.CarDrive
        fields = '__all__'


class CarConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = parceServer.models.CarCondition
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = parceServer.models.Color
        fields = '__all__'
