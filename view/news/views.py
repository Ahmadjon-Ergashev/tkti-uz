from django.db.models import F
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
        queryset = super().get_queryset().filter(status="pub").order_by("-added_at").select_related(
            "author", "update_user"
                ).prefetch_related(
                    "faculty_dact", "departments", "section_and_centers", "hashtag", "brm")
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
        news.News.objects.filter(slug=slug).update(post_viewed_count=F("post_viewed_count") + 1)
        object = news.News.objects.filter(slug=slug).select_related("author").first()
        return object
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context["object"]
        context["title"] = _("Yangilik")
        context["photos_list"] = _("Ko'proq rasmlarni ko'rish")
        context["news_photos"] = news.PhotoGallary.objects.filter(news=object).order_by("-added_at")[:10].select_related("news")
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
        queryset = super().get_queryset().filter(status="pub").order_by("-added_at").select_related("author", "update_user").prefetch_related("hashtag")
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
        news.Ads.objects.filter(slug=slug).update(post_viewed_count=F("post_viewed_count") + 1)
        object = get_object_or_404(news.Ads, slug=slug)
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
                img_objects = [
                    news.PhotoGallary(
                        news_id=news_id,
                        image=image
                    ) for image in data
                ]
                news.PhotoGallary.objects.bulk_create(img_objects)
            except Exception as e:
                print(e)
    return render(request, "widgets/upload_images.html") 


class PhotoGallaryView(ListView):
    """ photo gallary view """
    model = news.PhotoGallary
    template_name = "pages/photos/gallary.html"
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().order_by("-added_at").select_related("news")

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
        data = super().get_queryset().filter(news=news_id).order_by("-added_at").select_related("news")
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
        queryset = super().get_queryset().filter(status="pub").order_by("-added_at").select_related("author")
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
        news.VideoGallery.objects.filter(slug=slug).update(post_viewed_count=F("post_viewed_count") + 1)
        object = get_object_or_404(news.VideoGallery, slug=slug)
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
        queryset = super().get_queryset().filter(status="pub").order_by("added_at").select_related("author", "update_user", "event_type")
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
        news.Events.objects.filter(slug=slug).update(post_viewed_count=F("post_viewed_count") + 1)
        object = get_object_or_404(news.Events, slug=slug)
        return object
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_events"] = _("Barcha voqealar")
        return context
    