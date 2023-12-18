from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib.postgres import search as s
from django.views.generic.detail import DetailView
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404


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
    


class OpportunitiesView(TemplateView):
    template_name = "opportunities/main.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = _("Moliyaviy imtiyozlar")
        data["education_credit"] = _("Ta'lim kriditi")
        data["education_credit_opportunity"] = _("Talabalar uchun soliq imtiyozlari")
        return data


class EduCreditView(TemplateView):
    template_name = "opportunities/edu_credit.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = _("Ta'lim kriditi")
        return data


class CreditOpportView(TemplateView):
    template_name = "opportunities/credit_opport.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = _("Talabalar uchun soliq imtiyozlari")
        return data
    

class BRMItemsDetailView(DetailView):
    """ brm detail and filter by BRM """
    model = widgets.BRMItems
    template_name = "pages/news_and_ads/news_filter_brm.html"

    def get_object(self, queryset=None):
        pk = self.kwargs["pk"]
        obj = get_object_or_404(widgets.BRMItems, pk=pk)
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context["object"]
        context["title"] = object.name
        context["connected_news_title"] = _("Mavzuga aloqador yangiliklar.")
        context["connected_news"] = news.News.objects.filter(status=widgets.Status.published, brm=object.id).order_by("-added_at")
        return context
    