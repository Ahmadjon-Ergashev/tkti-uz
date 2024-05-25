from django.views import View
from django.db.models import Q, F
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404

# local
import main.models as models
from main.models import (posts, widgets, news)


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


class SearchAroundProgram(View):
    template_name = "widgets/search.html"

    def post(self, request):
        search_query = request.POST.get("search_query", "")

        titles = {
            "query": search_query,
            "ads_title": _("E'lonlar"),
            "posts_title": _("Postlar"),
            "shop_title": _("TKTI shop"),
            "events_title": _("Voqealar"),
            "news_title": _("Yangiliklar"),
            "title": _("Qidiruv natijalari"),
            "departments_title": _("Kafedralar"),
            "sections_title": _("Bo'lim va markazlar"),
            "not_found": _("Afsuski sizning so'rovingizga mos tushadigan ma'lumot topilmadi")
        }

        if not search_query:
            return render(request, self.template_name, titles | {"total": 0})

        query_conditions = Q(title__icontains=search_query) | Q(subtitle__icontains=search_query)

        news_objects = news.News.objects.filter(Q(status="pub") & query_conditions).only("title", "image", "slug")
        events_objects = models.Events.objects.filter(Q(status="pub") & query_conditions).only("title", "image", "slug")
        posts_objects = posts.Posts.objects.filter(Q(status="pub") & query_conditions).only("title", "image", "slug")
        ads_objects = news.Ads.objects.filter(Q(status="pub") & query_conditions).only("title", "image", "slug")
        shop_objects = models.Shop.objects.select_related("category").filter(name__icontains=search_query)
        sections_objects = models.SectionsAndCenters.objects.filter(
            title__icontains=search_query).only("title", "image", "slug")
        departments_objects = models.Departments.objects.filter(name__icontains=search_query).only("name", "slug")

        results = {
            "news": list(news_objects),
            "events": list(events_objects),
            "posts": list(posts_objects),
            "ads": list(ads_objects),
            "shop": list(shop_objects),
            "sections": list(sections_objects),
            "departments": list(departments_objects),
        }

        total = sum(len(items) for items in results.values())

        object_lists = {
            "total": total,
            "shop_objects": shop_objects,
            "ads_objects": ads_objects[:8],
            "news_objects": news_objects[:8],
            "posts_objects": posts_objects[:8],
            "events_objects": events_objects[:8],
            "sections_objects": sections_objects,
            "departments_objects": departments_objects,
        }

        context = titles | object_lists

        return render(request, self.template_name, context)


class SearchDetail(DetailView):
    template_name = "widgets/search_detail.html"

    def get_object(self, queryset=None):
        post_slug = self.kwargs["post_slug"]
        posts.Posts.objects.filter(slug=post_slug).update(post_viewed_count=F("post_viewed_count") + 1)
        obj = get_object_or_404(
            posts.Posts.objects.select_related("author", "update_user", "navbar"),
            slug=post_slug
        )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context["object"]
        try:
            extra_pdf_list = widgets.ExtraFile.objects.filter(
                post=post).only("name", "pdf_file")
            connected_faculty_dact = news.News.objects.filter(
                faculty_dact=post, status="pub").order_by("-added_at")[:12].only(
                "title", "slug", "added_at", "post_viewed_count").prefetch_related(
                "faculty_dact", "departments", "section_and_centers", "hashtag", "brm")
            context["extra_pdf_list"] = extra_pdf_list
            context["connected_faculty_dact"] = connected_faculty_dact
        except Exception as e:
            print(e, 141)
        if post.navbar:
            navbar = posts.Navbar.objects.get(slug=post.navbar.slug)
            context["title"] = navbar.name
            context["parent"] = navbar.parent.name
        else:
            context["title"] = post.title
            context["parent"] = ""

        context["depended_news"] = _("Mavzuga aloqador yangiliklar")
        context["bachelor_departments_way"] = posts.LearningWay.objects.filter(
            faculty=post, study_degree=1)
        context["master_departments_way"] = posts.LearningWay.objects.filter(
            faculty=post, study_degree=2
        )
        context["bachelor_departments_way_title"] = _("FAKULTETNING BAKALAVRIATURA YO‘NALISHLARI")
        context["master_departments_way_title"] = _("FAKULTETNING MAGISTRATURA YO‘NALISHLARI")
        context["faculty_title"] = _("Fakultet ma'muryati")
        context["departments_title"] = _("Fakultet kafedralari")
        try:
            context["extra_pdf_list"] = widgets.ExtraFile.objects.filter(
                post=post).only("name", "pdf_file")
        except Exception as e:
            print(e)
        try:
            if post.navbar:
                context["category_list"] = posts.Navbar.objects.filter(parent_id=navbar.parent.id)
            context["pdf_file"] = post.pdf_file.url
        except AttributeError:
            if post.navbar:
                context["category_list"] = navbar.get_children()
        except ValueError:
            context["pdf_file"] = ""
        return context


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
        context["connected_news"] = news.News.objects.filter(
            status=widgets.Status.published, brm=object.id).order_by("-added_at")
        context["extra_pdf_list"] = widgets.ExtraFile.objects.filter(
            brm_item=object
        ).order_by("-added_at")
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
