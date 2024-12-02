from django.db.models import F, Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import mixins, GenericViewSet

import main.models as models
import api.department_administration.serializers as serializers


class DepartmentAdministrationView(mixins.ListModelMixin, GenericViewSet):
    queryset = models.DepartmentAdministrationsNew.objects.select_related("department", "position")
    serializer_class = serializers.DepartmentAdmininstrationSerializer

    def get_queryset(self):
        qs = self.queryset.none()
        position = self.request.query_params.get("position")
        department = self.request.query_params.get("department")

        if position and department:
            qs = models.DepartmentAdministrationsNew.objects.filter(
                position=position, department=department
            )
        return qs
