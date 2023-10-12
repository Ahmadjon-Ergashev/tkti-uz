from typing import Any
from django.db import models
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404

# local models
from main.models.posts import (
    Posts, Status, Navbar, Departments
)
from main.models.widgets import (
    HeaderIMG, UsefullLinks, Statistika
)
from main.models.news import NewsAndAds



def Home(request):
    """ for home page view """
    context = {
        "all": _("Barchasi"),
        "title": _("Bosh sahifa"),
        "ads_section_title": _("E'lonlar"),
        "news_section_title": _("Yangiliklar"),
        "header_img": HeaderIMG.objects.all().order_by("order_num"),
        "statistika": Statistika.objects.all().order_by("-added_at"),
        "usefull_links": UsefullLinks.objects.all().order_by("-add_time"),
        "top_3_ads": NewsAndAds.objects.filter(object_type="ads", status="pub").order_by("-added_at")[:3],
        "last_news_6": NewsAndAds.objects.filter(object_type="news", status="pub").order_by("-added_at")[:6],
        "top_3_news": NewsAndAds.objects.filter(object_type="news", status="pub").order_by("-post_viewed_count")[:3],
    }
    return render(request, "home.html", context)


class PostsListView(ListView):
    """ get all posts what connected to navbar """
    model = Posts
    paginate_by = 5
    ordering = ["-added_at"]
    template_name = "pages/posts/posts.html"

    def get_queryset(self):
        navbar_slug = self.kwargs["navbar_slug"]
        qs = super().get_queryset().filter(status=Status.published, navbar__slug=navbar_slug).order_by("-added_at")
        return qs 
    
    def get_context_data(self, **kwargs):
        navbar_name = Navbar.objects.get(slug=self.kwargs["navbar_slug"])
        context = super().get_context_data(**kwargs)
        context["title"] = navbar_name.name
        context["parent"] = navbar_name.parent
        context["title_slug"] = navbar_name.slug
        try:
            context["category_list"] = Navbar.objects.filter(parent_id=navbar_name.parent.id)
        except AttributeError:
            context["category_list"] = navbar_name.get_children()
        try:
            context["pdf_file"] = context["object_list"][0].pdf_file
        except IndexError:
            context["pdf_file"] = ""
        print(context["category_list"])
        context["home"] = _("Asosiy sahifa")
        context["empty"] = _("Afsuski hozircha ma'lumotlar topilmadi :(")
        return context


class PostDetailView(DetailView):
    """ get detail of posts """
    model = Posts
    template_name = "pages/posts/post_detail.html"

    def get_object(self, queryset=None):
        post_slug = self.kwargs["post_slug"]
        obj = get_object_or_404(Posts, slug=post_slug)
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context["object"]
        navbar = Navbar.objects.get(slug=post.navbar.slug)
        context["title"] = navbar.name
        context["faculty_title"] = _("Fakultet ma'muryati")
        context["departments_title"] = _("Fakultet kafedralari")
        context["parent"] = navbar.parent.name
        try:
            context["category_list"] = Navbar.objects.filter(parent_id=navbar.parent.id)
            context["pdf_file"] = post.pdf_file.url
        except AttributeError:
            context["category_list"] = navbar.get_children()
        except ValueError:
            context["pdf_file"] = ""
        return context

class DepartmentsDetailView(DetailView):
    """ departments detail view """
    model = Departments
    template_name = "pages/posts/departments_detail.html"

    def get_object(self, queryset):
        dept_slug = self.kwargs['dept_slug']
        obj = get_object_or_404(Departments, slug=dept_slug)
        return obj