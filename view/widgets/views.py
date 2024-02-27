from django.views import View
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

    def get_queryset(self):
        qs = super().get_queryset().only("title", "description")
        return qs

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
from django.shortcuts import render


# class SearchAroundProgram(View):
#     template_name = "widgets/search.html"
#
#     def post(self, request, *args, **kwargs):
#         search_query = request.POST.get("search_query", "")
#         vector = s.SearchVector("title", "subtitle", config="english")
#         query = s.SearchQuery(search_query)
#         posts_results = posts.Posts.objects.annotate(search=vector).filter(search=query).only(
#             "title", "image", "slug"
#         )
#         news_results = news.News.objects.annotate(search=vector).filter(search=query).only(
#             "title", "image", "slug"
#         )
#         ads_results = news.Ads.objects.annotate(search=vector).filter(search=query).only(
#             "title", "image", "slug"
#         )
#         events_results = news.Events.objects.annotate(search=vector).filter(search=query).only(
#             "title", "image", "slug"
#         )
#         combined_results = list(chain(posts_results, news_results, ads_results, events_results))
#         context = {
#             "search_results": combined_results,
#             "title": _("Qidituv natijalari"),
#             "not_found_404": _("Afsuski hechqanday ma'lumot topilmadi :(")
#         }
#         return render(request, self.template_name, context)
#

class SearchAroundProgram(View):
    template_name = "widgets/search.html"

    def post(self, request, *args, **kwargs):
        search_query = request.POST.get("search_query", "")
        vector = s.SearchVector("title", "subtitle", config='english')
        query = s.SearchQuery(search_query)

        posts_results = posts.Posts.objects.annotate(search=vector).filter(search=query)
        news_results = news.News.objects.annotate(search=vector).filter(search=query)
        ads_results = news.Ads.objects.annotate(search=vector).filter(search=query)
        events_results = news.Events.objects.annotate(search=vector).filter(search=query)

        combined_results = list(chain(posts_results, news_results, ads_results, events_results))

        context = {
            "search_results": combined_results,
            "title": _("Qidituv natijalari"),
            "not_found_404": _("Afsuski hechqanday ma'lumot topilmadi :(")
        }
        return render(request, self.template_name, context)


class SearchDetail(DetailView):
    template_name = "widgets/search_detail.html"

    def get_object(self, queryset=None):
        slug = self.kwargs["slug"]
        print(slug)
        if len(posts.Posts.objects.filter(slug=slug)) != 0:
            return posts.Posts.objects.filter(slug=slug).first()
        
        elif len(news.News.objects.filter(slug=slug)) != 0:
            return news.News.objects.filter(slug=slug).first()
        
        elif len(news.Ads.objects.filter(slug=slug)) != 0:
            return news.Ads.objects.filter(slug=slug).first()
        
        elif len(news.Events.objects.filter(slug=slug)) != 0:
            return news.Events.objects.filter(slug=slug).first()
        
        return None
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        obj = data["object"]
        try:
            data["conn_section_and_centers"] = news.News.objects.filter(
                section_and_centers=obj.id, status="pub").order_by("-added_at")[:12].only(
                    "title", "slug", "added_at", "post_viewed_count").prefetch_related(
                        "faculty_dact", "departments", "section_and_centers", "hashtag", "brm")
        except Exception as e:
            print(e, 141)     
        try:
            navbar = posts.Navbar.objects.get(slug=obj.navbar.slug)
            data["parent"] = navbar.parent.name
        except Exception as e:
            ...
        data["depended_news"] = _("Mavzuga aloqador yangiliklar") 
        return data


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


class FinancialBenefitView(View):
    template_name = "opportunities/main.html"

    def get(self, request, *args, **kwargs):
        objects = widgets.FinancialBenefit.objects.all()
        return render(request, self.template_name, {
            "objects_list": objects,
            "title": _("Moliyaviy imtiyozlar")
        })


class FinancialBenefitDetailView(View):
    template_name = "opportunities/credit_opport.html"

    def get(self, request, *args, **kwargs):
        translation_words = {
            "about": _("Imtiyoz haqida"),
            "responsible_org": _("Mas’ul tashkilot"),
            "who_for": _("Kimlar uchun"),
            "order_and_time": _("Imtiyozni taqdim etish tartibi va muddatlari"),
            "lower_base": _("Huquqiy asos"),
            "contact": _("Aloqa ma’lumotlari")
        }
        pk = self.kwargs.get("pk")
        if pk:
            obj = widgets.FinancialBenefit.objects.filter(pk=pk).first()
            data = {"object": obj, "title": obj.name}
            context = translation_words | data
            return render(request, self.template_name, context)
