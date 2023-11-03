from rest_framework import viewsets, mixins
from drf_yasg.utils import swagger_auto_schema

# local apps
from main.models import widgets
from api.widgets import serializers, query_params


class YearView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ view for year """
    queryset = widgets.Year.objects.all()
    serializer_class = serializers.YearSerializers


class FaqCategoryView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ view for faq category """
    queryset = widgets.FaqCategory.objects.all()
    serializer_class = serializers.FaqCategorySerializers


class FaqView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ view for faq """
    queryset = widgets.Faq.objects.all()
    serializer_class = serializers.FaqSeralizers

    def get_queryset(self):
        queryset = super().get_queryset().none()
        faq_category = self.request.query_params.get("faq_category")
        if faq_category:
            queryset = super().get_queryset().filter(category=faq_category, is_active=True).all()
        return queryset
    
    @swagger_auto_schema(manual_parameters=query_params.faq_params())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    


