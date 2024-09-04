from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

import main.models as models


class DepartmentAdministrationPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DepartmentAdministrationsPositions
        fields = '__all__'


class DepartmentAdmininstrationSerializer(serializers.ModelSerializer):
    position = DepartmentAdministrationPositionSerializer()

    class Meta:
        model = models.DepartmentAdministrationsNew
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["view"] = _("Ma'lumotnoma")
        return data
