from django.utils import timezone
from rest_framework import serializers
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _


from main.models import news
from api.widgets.serializers import EventTypeSerializers


class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = news.News
        fields = ["id", "title", "image", "slug", "post_viewed_count", "added_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["read_more"] = _("Batafsil")
        local_time = timezone.localtime(instance.added_at)
        data["added_at"] = local_time.strftime("%Y-%m-%d %H:%M")
        return data
    

class AdsSerializers(serializers.ModelSerializer):
    class Meta:
        model = news.Ads
        fields = ["id", "title", "image", "slug", "post_viewed_count", "added_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        local_time = timezone.localtime(instance.added_at)
        data["added_at"] = local_time.strftime("%Y-%m-%d %H:%M")
        return data
    

class VideoSerializers(serializers.ModelSerializer):
    class Meta: 
        model = news.VideoGallery
        fields = ["id", "title", "poster", "post_viewed_count", "slug", "added_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        local_time = timezone.localtime(instance.added_at)
        data["added_at"] = local_time.strftime("%Y-%m-%d %H:%M")
        return data


class EventsSerializers(serializers.ModelSerializer):
    event_type = EventTypeSerializers(read_only=True)

    class Meta:
        model = news.Events
        fields = ["id", "title", "location", "event_type", "slug", "added_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        local_time = timezone.localtime(instance.added_at)
        data["added_at"] = local_time.strftime("%Y-%m-%d %H:%M")
        data["read_more"] = _("Batafsil")
        return data
