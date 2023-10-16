from rest_framework.generics import ListAPIView


# local apps
from main.models.widgets import Year
from .serializers import YearSerializers


class YearView(ListAPIView):
    """ view for year """
    queryset = Year.objects.all()
    serializer_class = YearSerializers