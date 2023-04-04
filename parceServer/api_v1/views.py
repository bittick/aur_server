from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView
from parceServer.models import *
from parceServer.api_v1.serializers import *
from parceServer.api_v1.filters import CarAdFilter
from rest_framework import filters
from .paginators import CarAdPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response


class CarAdFilteredList(ListAPIView):
    serializer_class = CarAdSerializer
    queryset = CarAd.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CarAdFilter
    ordering_fields = ['price', 'production_date', 'mileage', 'create_date']
    ordering = ['-create_date']
    search_fields = ['title', 'description']
    pagination_class = CarAdPagination


class CarAdDetailView(RetrieveAPIView):
    serializer_class = CarAdSerializer
    queryset = CarAd.objects.all()
    lookup_field = 'ad_id'


class BrandList(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class AllModelsByBrand(ListAPIView):
    serializer_class = BrandSerializer

    def get_queryset(self):
        return Brand.objects.prefetch_related('carmodel_set').all()


class ModelsByBrand(ListAPIView):
    serializer_class = CarModelSerializer

    def get_queryset(self):
        brand_name = self.kwargs['brand']
        return CarModel.objects.filter(brand__name=brand_name)


@api_view(['GET'])
def get_field_lists(request, item):
    field_list = {
        'cars_engine': [Engine, EngineSerializer],
        'cars_gearbox': [Gearbox, GearboxSerializer],
        'cars_type': [CarType, CarTypeSerializer],
        'cars_drive': [CarDrive, CarDriveSerializer],
        'condition': [CarCondition, CarConditionSerializer],
        'color': [Color, ColorSerializer],
    }
    current_item = field_list.get(item)
    if not current_item:
        return Response(status=404)
    model, serializer = current_item
    queryset = model.objects.all()
    return Response(
        [serializer(obj).data for obj in queryset],
        status=200,
    )
