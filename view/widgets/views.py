from django.views.generic.list import ListView
from django.contrib.postgres import search as s
from django.utils.translation import gettext_lazy as _

# local
from main.models import posts, widgets, news


class SiteMapView(ListView):
    model = posts.Navbar
    template_name = "widgets/site_map.html"    
    ordering = "name"

    def get_queryset(self):
        data = super().get_queryset().filter(status="base", visible=True).order_by("order_num")
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Sayt haritasi")
        return context
    

class FlagView(ListView):
    model = widgets.Flag
    template_name = "widgets/flag.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("O`zbekiston Respublikasining davlat bayrog`i")
        return context
    

class CoatofArmsView(ListView):
    model = widgets.CoatofArms
    template_name = "widgets/coat_of_arms.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("O`zbekiston Respublikasining davlat gerbi")
        return context
    

class AnthemView(ListView):
    model = widgets.Anthem
    template_name = "widgets/anthem.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("O`zbekiston Respublikasining davlat madhiyasi")
        return context
    

class FaqView(ListView):
    model = widgets.FaqCategory
    template_name = "widgets/faq.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = _("Ko'p beriladigan savollar")
        return data
    

# searching multiple model
from itertools import chain
from django.shortcuts import redirect, render


class SearchAroundProgram(ListView):
    template_name = "widgets/search.html"
    
    def post(self, request, *args, **kwargs):
        search_query = request.POST.get("search_query", "")
        vector = s.SearchVector("title", "subtitle")
        query = s.SearchQuery(search_query)
        posts_results = posts.Posts.objects.annotate(search=vector).filter(search=query)
        news_results = news.News.objects.annotate(search=vector).filter(search=query)
        ads_results = news.Ads.objects.annotate(search=vector).filter(search=query)
        combined_results = list(chain(posts_results, news_results, ads_results))
        context = {
            "search_results": combined_results,
            "title": _("Qidituv natijalari"),
            "not_found_404": _("Afsuski hechqanday ma'lumot topilmadi :(")
        }
        return render(request, self.template_name, context)