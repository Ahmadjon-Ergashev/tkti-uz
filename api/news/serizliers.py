from rest_framework import serializers


from main.models import news

class NewsSerizliers(serializers.ModelSerializer):
    class Meta:
        model = news.News
        fields = ["id", "title", "image", "slug", "post_viewed_count", "added_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["added_at"] = instance.added_at.strftime("%Y-%m-%d %H:%M")
        return data
    


class AdsSerizliers(serializers.ModelSerializer):
    class Meta:
        model = news.Ads
        fields = ["id", "title", "image", "slug", "post_viewed_count", "added_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["added_at"] = instance.added_at.strftime("%Y-%m-%d %H:%M")
        return data
    

class VideoSerializers(serializers.ModelSerializer):
    class Meta:
        model = news.VideoGallery
        fields = ["id", "title", "video_file", "poster", "added_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["added_at"] = instance.added_at.strftime("%Y-%m-%d %H:%M")
        return data
