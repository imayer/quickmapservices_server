import os
from rest_framework.filters import SearchFilter, DjangoFilterBackend, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, OrderedDict
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from ...icon_renderer import IconRenderer
from ...icon_serializer import IconSerializer
from ...models import GeoService, TmsService, WmsService, WfsService, ServiceIcon, GeoJsonService


# === Serializers

class GeoServiceSerializer(ModelSerializer):
    class Meta:
        model = GeoService
        fields = ('id', 'guid', 'name', 'desc', 'type', 'epsg', 'icon', 'submitter', 'created_at', 'updated_at')


class TmsServiceSerializer(ModelSerializer):
    class Meta:
        model = TmsService
        fields = '__all__'


class WmsServiceSerializer(ModelSerializer):
    class Meta:
        model = WmsService
        fields = '__all__'


class WfsServiceSerializer(ModelSerializer):
    class Meta:
        model = WfsService
        fields = '__all__'


class GeoJsonServiceSerializer(ModelSerializer):
    class Meta:
        model = GeoJsonService
        fields = '__all__'


class ServiceIconSerializer(ModelSerializer):
    class Meta:
        model = ServiceIcon
        fields = ('id', 'guid', 'name')


class GeoServiceBoundarySerializer(ModelSerializer):
    class Meta:
        model = GeoService
        fields = ('boundaries',)


# === Views Geoservices

class GeoServiceListView(ListAPIView):
    queryset = GeoService.objects.all()
    serializer_class = GeoServiceSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filter_fields = ('type', 'epsg', 'submitter')
    search_fields = ('name', 'desc')
    ordering_fields = ('id', 'name', 'created_at', 'updated_at')
    ordering = ('name',)


class GeoServiceDetailedView(RetrieveAPIView):
    queryset = GeoService.objects\
        .select_related('tmsservice')\
        .select_related('wmsservice')\
        .select_related('wfsservice')\
        .select_related('geojsonservice')

    def get_object(self):
        obj = super(GeoServiceDetailedView, self).get_object()
        if obj:
            if obj.type == TmsService.service_type:
                obj = obj.tmsservice
            if obj.type == WmsService.service_type:
                obj = obj.wmsservice
            if obj.type == WfsService.service_type:
                obj = obj.wfsservice
            if obj.type == GeoJsonService.service_type:
                obj = obj.geojsonservice
        return obj

    def get_serializer(self, instance):
        if instance:
            if instance.type == TmsService.service_type:
                return TmsServiceSerializer(instance)
            if instance.type == WmsService.service_type:
                return WmsServiceSerializer(instance)
            if instance.type == WfsService.service_type:
                return WfsServiceSerializer(instance)
            if instance.type == GeoJsonService.service_type:
                return GeoJsonServiceSerializer(instance)

        return GeoServiceSerializer(instance)


class GeoServiceBoundaryView(RetrieveAPIView):
    queryset = GeoService.objects.all()
    serializer_class = GeoServiceBoundarySerializer


# === Views Icons

class ServiceIconListView(ListAPIView):
    queryset = ServiceIcon.objects.all()
    serializer_class = ServiceIconSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)


class ServiceIconDetailedView(RetrieveAPIView):
    queryset = ServiceIcon.objects.all()
    serializer_class = ServiceIconSerializer


class IconRetrieveView(RetrieveAPIView):
    queryset = ServiceIcon.objects.all()
    serializer_class = IconSerializer
    renderer_classes = [IconRenderer, ]


class DefaultIconRetrieveView(APIView):
    renderer_classes = [IconRenderer, ]

    def get(self, request, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return Response(open(os.path.join(BASE_DIR, os.pardir, 'static/qms_core/img/default_icon.png'), mode='rb'))


# === API ROOT and others

class ApiRootView(APIView):

    def get(self, request, format=None):
        temp_rep_val = 2110112
        simple_url = lambda name: reverse(name, request=request, format=format)
        repl_id_ulr = lambda name: reverse(name,
                                           kwargs={'pk': temp_rep_val},
                                           request=request,
                                           format=format).replace(str(temp_rep_val), '{id}')

        return Response(OrderedDict((
            ('geoservices_url', simple_url('geoservice_list')),
            ('geoservices_type_filter_url', simple_url('geoservice_list') + '?type={tms|wms|wfs|geojson}'),
            ('geoservices_epsg_filter_url', simple_url('geoservice_list') + '?epsg={any_epsg_code}'),
            ('geoservices_search_url', simple_url('geoservice_list') + '?search={q}'),
            ('geoservices_ordering_url', simple_url('geoservice_list') + '?ordering={name|-name|id|-id|created_at|-created_at|updated_at|-updated_at'),
            ('geoservices_pagination_url', simple_url('geoservice_list') + '?limit={int}&offset={int}'),
            ('geoservice_detail_url', repl_id_ulr('geoservice_detail')),
            ('icons_url', simple_url('service_icon_list')),
            ('icons_search_url', simple_url('service_icon_list') + '?search={q}'),
            ('icons_pagination_url', simple_url('service_icon_list') + '?limit={int}&offset={int}'),
            ('icon_detail_url', repl_id_ulr('service_icon_detail')),
            ('icon_content_url', repl_id_ulr('service_icon_retrieve')),
            ('icon_resized_content_url', repl_id_ulr('service_icon_retrieve') + '?width={16<=x<=64}&height={16<=y<=64}'),
            ('default_icon_url', simple_url('service_icon_default'))
        )))
