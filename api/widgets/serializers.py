from rest_framework import serializers


from main.models import widgets



class YearSerializers(serializers.ModelSerializer):
    class Meta:
        model = widgets.Year
        fields = "__all__"
    

class FaqCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = widgets.FaqCategory
        fields = "__all__"


class FaqSeralizers(serializers.ModelSerializer):
    class Meta:
        model = widgets.Faq
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["answer"] = instance.answer.html
        return data