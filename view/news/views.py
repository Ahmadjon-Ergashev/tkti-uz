from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.utils.translation import gettext_lazy as _


# local vars
from main.models.news import NewsAndAds


class NewsDetailView(DetailView):
    """ detail view for news and detail """
    model = NewsAndAds
    template_name = "pages/news_and_ada/detail.html"

    def get_object(self, queryset=None):
        slug = self.kwargs["obj_slug"]
        object = get_object_or_404(NewsAndAds, slug=slug)
        object.post_viewed_count += 1
        object.save()
        return object
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context["object"]
        context["title"] = _("Yangilik") if object.object_type == "news" else _("E'lon")
        try:
            domain = self.request.get_host()
            context["pdf_file"] = f"https://{domain}" + object.pdf_file.url
        except ValueError:
            context["pdf_file"] = ""
        return context