from rest_framework import viewsets, mixins

# local apps
from main.models import widgets
from .serializers import YearSerializers


class YearView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ view for year """
    queryset = widgets.Year.objects.all()
    serializer_class = YearSerializers