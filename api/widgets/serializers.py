from rest_framework import serializers


from main.models.widgets import Year



class YearSerializers(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = "__all__"
    