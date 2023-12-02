from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _


# local vars
from main.models import news, widgets


class NewsView(ListView):
    """ all news view with pagination """
    model = news.News
    template_name = "pages/news_and_ads/all_items.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(status="pub").order_by("-added_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Yangiliklar")
        context["data_number"] = 0
        return context


class NewsDetailView(DetailView):
    """ detail view for news and detail """
    model = news.News
    template_name = "pages/news_and_ads/detail.html"

    def get_object(self, queryset=None):
        slug = self.kwargs["obj_slug"]
        object = get_object_or_404(news.News, slug=slug)
        object.post_viewed_count += 1
        object.save()
        return object
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context["object"]
        context["title"] = _("Yangilik")
        context["photos_list"] = _("Ko'proq rasmlarni ko'rish")
        context["news_photos"] = news.PhotoGallary.objects.filter(news=object).order_by("-added_at")[:10]
        try:
            domain = self.request.get_host()
            context["pdf_file"] = f"http://{domain}" + object.pdf_file.url
        except ValueError:
            context["pdf_file"] = ""
        return context


class HashtagSearchView(ListView):
    """ search by hashtags in news """
    model = news.News
    template_name = "pages/news_and_ads/all_items.html"

    def get_queryset(self):
        hashtag = self.kwargs["hashtag"]
        hashtag_ = widgets.Hashtag.objects.get(name=hashtag)
        data =  super().get_queryset().filter(hashtag=hashtag_)
        return data    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Yangiliklar")
        context["data_number"] = 0
        return context




class AdsView(ListView):
    """ all ads items with pagination """
    model = news.Ads
    template_name = "pages/news_and_ads/all_items.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(status="pub").order_by("-added_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("E'lonlar")
        context["data_number"] = 1
        return context


class AdsDetailView(DetailView):
    """ detail view for ads and detail """
    model = news.News
    template_name = "pages/news_and_ads/detail.html"

    def get_object(self, queryset=None):
        slug = self.kwargs["obj_slug"]
        object = get_object_or_404(news.Ads, slug=slug)
        object.post_viewed_count += 1
        object.save()
        return object
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context["object"]
        context["title"] = _("E'lon")
        try:
            domain = self.request.get_host()
            context["pdf_file"] = f"http://{domain}" + object.pdf_file.url
        except ValueError:
            context["pdf_file"] = ""
        return context
    

def Upload_Images(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                data = request.FILES.getlist('images') 
                news_id = int(request.POST.get("news_list_id"))
                news_obj = news.News.objects.get(id=news_id)
                for d in data:
                    img = news.PhotoGallary.objects.create(news=news_obj, image=d)
                    img.save()
            except Exception as e:
                print(e)
    return render(request, "widgets/upload_images.html") 


class PhotoGallaryView(ListView):
    """ photo gallary view """
    model = news.PhotoGallary
    template_name = "pages/photos/gallary.html"
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().order_by("-added_at")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = _("Rasmlar")
        return data


class PhotoGallaryFilterView(ListView):
    """ photo gallary view """
    model = news.PhotoGallary
    template_name = "pages/photos/gallary.html"
    paginate_by = 20

    def get_queryset(self):
        news_id = self.kwargs["news_id"]
        data = super().get_queryset().filter(news=news_id).order_by("-added_at")
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = _("Rasmlar")
        return data
    

class VideoView(ListView):
    """ all videos """
    model = news.VideoGallery
    template_name = "pages/news_and_ads/all_items.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(status="pub").order_by("-added_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Video lavhalar")
        context["data_number"] = 2
        return context


class VideosDetailView(DetailView):
    """ videos detail """
    model = news.VideoGallery
    template_name = "pages/news_and_ads/detail.html"

    def get_object(self, queryset=None):
        slug = self.kwargs["obj_slug"]
        object = get_object_or_404(news.VideoGallery, slug=slug)
        object.post_viewed_count += 1
        object.save()
        return object
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Video lavhalar")
        return context
    

class EventsView(ListView):
    model = news.Events
    template_name = "pages/events/events_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(status="pub").order_by("added_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Voqealar")
        context["read_more"] = _("Batafsil")
        return context
    

class EventsDetailView(DetailView):
    model = news.Events
    template_name = "pages/events/events_detail.html"

    def get_object(self, queryset=None):
        slug = self.kwargs["slug"]
        object = get_object_or_404(news.Events, slug=slug)
        object.post_viewed_count += 1
        object.save()
        return object
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_events"] = _("Barcha voqealar")
        return context
    