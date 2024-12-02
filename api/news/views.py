from django.db.models import F, Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import mixins, GenericViewSet

from main.models import news
from api.news import serizliers
from api.news import query_params


class NewsView(mixins.ListModelMixin, GenericViewSet):
    queryset = news.News.objects.select_related(
        "author", "update_user").prefetch_related(
        "faculty_dact", "departments", "section_and_centers", "hashtag", "brm")
    serializer_class = serizliers.NewsSerializers

    def get_queryset(self):
        qs = self.queryset.none()
        search = self.request.query_params.get("search")
        get_type = self.request.query_params.get("get_type")
        end = self.request.query_params.get("end")
        start = self.request.query_params.get("start")
        start = 0 if start is None else start
        if search:
            qs = self.queryset.filter(Q(status="pub") & Q(title__icontains=search) | Q(subtitle__icontains=search))
        if get_type and end or start:
            if get_type == query_params.GetType.latest.value:
                qs = self.queryset.filter(status="pub").order_by("-added_at")[int(start):int(end)]
            elif get_type == query_params.GetType.most_read.value:
                qs = self.queryset.filter(status="pub").order_by("-post_viewed_count")[int(start):int(end)]
        return qs

    @swagger_auto_schema(manual_parameters=query_params.news_queries())
    def list(self, request, *args, **kwargs):
        return super(NewsView, self).list(request, *args, **kwargs)


class AdsView(mixins.ListModelMixin, GenericViewSet):
    queryset = news.Ads.objects.all()
    serializer_class = serizliers.AdsSerializers

    def get_queryset(self):
        qs = super().get_queryset().none()
        get_type = self.request.query_params.get("get_type")
        end = self.request.query_params.get("end")
        start = self.request.query_params.get("start")
        start = 0 if start == None else start
        if get_type and end or start:
            if get_type == query_params.GetType.latest.value:
                return super().get_queryset().filter(status="pub").order_by("-added_at")[int(start):int(end)]
            elif get_type == query_params.GetType.most_read.value:
                return super().get_queryset().filter(status="pub").order_by("-post_viewed_count")[int(start):int(end)]
        return qs

    @swagger_auto_schema(manual_parameters=query_params.news_queries())
    def list(self, request, *args, **kwargs):
        return super(AdsView, self).list(request, *args, **kwargs)


class VideoView(mixins.ListModelMixin, GenericViewSet):
    queryset = news.VideoGallery.objects.all()
    serializer_class = serizliers.VideoSerializers

    def get_queryset(self):
        qs = super().get_queryset().none()
        get_type = self.request.query_params.get("get_type")
        end = self.request.query_params.get("end")
        start = self.request.query_params.get("start")
        start = 0 if start == None else start
        if get_type and end or start:
            if get_type == query_params.GetType.latest.value:
                return super().get_queryset().filter(status="pub").order_by("-added_at")[int(start):int(end)]
            elif get_type == query_params.GetType.most_read.value:
                return super().get_queryset().filter(status="pub").order_by("-post_viewed_count")[int(start):int(end)]
        return qs

    @swagger_auto_schema(manual_parameters=query_params.news_queries())
    def list(self, request, *args, **kwargs):
        return super(VideoView, self).list(request, *args, **kwargs)


""" Events SECTION """
from datetime import datetime
from django.utils import timezone


class EventView(mixins.ListModelMixin, GenericViewSet):
    queryset = news.Events.objects.all()
    serializer_class = serizliers.EventsSerializers

    def get_queryset(self):
        qs = super().get_queryset().none()
        end = self.request.query_params.get("end")
        start = self.request.query_params.get("start")
        get_type = self.request.query_params.get("get_type")
        if get_type and start and end:
            if get_type == query_params.EventGetType.all.value:
                qs = super().get_queryset().filter(status='pub').order_by('-added_at')[int(start):int(end)]
            elif get_type == query_params.EventGetType.upcoming.value:
                qs = super().get_queryset().filter(status='pub', added_at__gte=timezone.now()).order_by('added_at')[
                     int(start):int(end)]
            elif get_type == query_params.EventGetType.past.value:
                qs = super().get_queryset().filter(status='pub', added_at__lte=timezone.now()).order_by('-added_at')[
                     int(start):int(end)]
        return qs.annotate(
            event_type_name=F("event_type__name")
        )

    @swagger_auto_schema(manual_parameters=query_params.events_queries())
    def list(self, request, *args, **kwargs):
        return super(EventView, self).list(request, *args, **kwargs)
