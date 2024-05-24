from django.views import View
from django.db.models import Q
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import main.models as models


class SearchingListNewsView(View):
    template_name = 'widgets/searching_list.html'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        search_query = kwargs.get('query')
        objects = models.News.objects.filter(
            Q(status="pub") & Q(title__icontains=search_query) | Q(subtitle__icontains=search_query))

        paginator = Paginator(objects, self.paginate_by)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            "url": "/news/detail",
            "object_list": page_obj,
            "title": _("Yangiliklar"),
        }
        return render(request, self.template_name, context)


class SearchingAdsNewsView(View):
    template_name = 'widgets/searching_list.html'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        search_query = kwargs.get('query')
        objects = models.Ads.objects.filter(
            Q(status="pub") & Q(title__icontains=search_query) | Q(subtitle__icontains=search_query))

        paginator = Paginator(objects, self.paginate_by)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            "url": "/ads/detail",
            "object_list": page_obj,
            "title": _("E'lonlar"),
        }
        return render(request, self.template_name, context)


class SearchingEventsNewsView(View):
    template_name = 'widgets/searching_list.html'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        search_query = kwargs.get('query')
        objects = models.Events.objects.filter(
            Q(status="pub") & Q(title__icontains=search_query) | Q(subtitle__icontains=search_query))

        paginator = Paginator(objects, self.paginate_by)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            "url": "/events/detail",
            "object_list": page_obj,
            "title": _("Voqealar"),
        }
        return render(request, self.template_name, context)


class SearchingPostsNewsView(View):
    template_name = 'widgets/searching_list.html'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        search_query = kwargs.get('query')
        objects = models.Posts.objects.filter(
            Q(status="pub") & Q(title__icontains=search_query) | Q(subtitle__icontains=search_query))

        paginator = Paginator(objects, self.paginate_by)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            "url": "/searching/results/detail",
            "object_list": page_obj,
            "title": _("Postlar"),
        }
        return render(request, self.template_name, context)



