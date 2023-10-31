from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404

# local models
from main.models import (
    posts, news, widgets
)


def Home(request):
    """ for home page view """
    translate_words = {
        "all": _("Barchasi"),
        "search": _("Qidirish"),
        "title": _("Bosh sahifa"),
        "sp_year": _("Yilni tanlang"),
        "high_degree": _("Bakalavriat"),
        "faculty_title": _("Fakultetlar"),
        "sp_dept": _("Kafedrani tanlang"),
        "ads_section_title": _("E'lonlar"),
        "higher_degree": _("Magistraturat"),
        "sp_type": _("Ta'lim turini tanlang"),
        "sp_faculty": _("Fakultetni tanlang"),
        "videos_section_title": _("Videolar"),
        "the_most_read": _("Top yangiliklar"),
        "photo_grid_title": _("Foto lavhalar"),
        "nth_faculty": _("tarkibidagi kafedralar"),
        "the_last_news": _("Eng so'ngi yangiliklar"),
        "study_way_title": _("Ta'lim dasturi katalogi"),
        "not_found_404": _("Afsuski hechqanday ma'lumot topilmadi :("),
    }
    objects_list = {
        "header_img": widgets.HeaderIMG.objects.all().order_by("order_num"),
        "statistika": widgets.Statistika.objects.all().order_by("-added_at"),
        "usefull_links": widgets.UsefullLinks.objects.all().order_by("-add_time"),
        "top_3_ads": news.Ads.objects.filter(status="pub").order_by("-added_at")[:3],
        "last_news_6": news.News.objects.filter(status="pub").order_by("-added_at")[:8],
        "the_photos_home": widgets.PhotoGallary.objects.order_by("-added_at")[:6].all(),
        "top_3_news": news.News.objects.filter(status="pub").order_by("-post_viewed_count")[:4],
        "the_last_ads_4": news.Ads.objects.filter(status="pub").order_by("-added_at")[:4].all(),
        "the_last_news_4": news.News.objects.filter(status="pub").order_by("-added_at")[:4].all(),
        "the_last_ads_8": news.Ads.objects.filter(status="pub").order_by("-added_at")[4:12].all(),
        "the_last_news_8": news.News.objects.filter(status="pub").order_by("-added_at")[4:12].all(),
        "the_videos": news.VideoGallery.objects.filter(status="pub").order_by("-added_at")[:6].all(),
        "the_most_read_4": news.News.objects.filter(status="pub").order_by("-post_viewed_count")[:4].all(),
        "the_most_read_8": news.News.objects.filter(status="pub").order_by("-post_viewed_count")[4:12].all(),
    }
    context = translate_words | objects_list        
    return render(request, "home.html", context)



class PostsListView(ListView):
    """ get all posts what connected to navbar """
    model = posts.Posts
    paginate_by = 5
    ordering = ["-added_at"]
    template_name = "pages/posts/posts.html"

    def get_queryset(self):
        navbar_slug = self.kwargs["navbar_slug"]
        qs = super().get_queryset().filter(status=widgets.Status.published, navbar__slug=navbar_slug).order_by("-added_at")
        return qs 
    
    def get_context_data(self, **kwargs):
        navbar_name = posts.Navbar.objects.get(slug=self.kwargs["navbar_slug"])
        context = super().get_context_data(**kwargs)
        context["title"] = navbar_name.name
        context["parent"] = navbar_name.parent
        context["title_slug"] = navbar_name.slug
        try:
            context["category_list"] = posts.Navbar.objects.filter(parent_id=navbar_name.parent.id)
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
    model = posts.Posts
    template_name = "pages/posts/post_detail.html"

    def get_object(self, queryset=None):
        post_slug = self.kwargs["post_slug"]
        obj = get_object_or_404(posts.Posts, slug=post_slug)
        obj.post_viewed_count += 1
        obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context["object"]
        navbar = posts.Navbar.objects.get(slug=post.navbar.slug)
        context["title"] = navbar.name
        context["faculty_title"] = _("Fakultet ma'muryati")
        context["departments_title"] = _("Fakultet kafedralari")
        context["parent"] = navbar.parent.name
        try:
            context["category_list"] = posts.Navbar.objects.filter(parent_id=navbar.parent.id)
            context["pdf_file"] = post.pdf_file.url
        except AttributeError:
            context["category_list"] = navbar.get_children()
        except ValueError:
            context["pdf_file"] = ""
        return context

class DepartmentsDetailView(DetailView):
    """ departments detail view """
    model = posts.Departments
    template_name = "pages/posts/departments_detail.html"

    def get_object(self, queryset=None):
        dept_slug = self.kwargs['dept_slug']
        obj = get_object_or_404(posts.Departments, slug=dept_slug)
        obj.post_viewed_count += 1
        obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context["object"]
        context["departments_list"] = posts.Departments.objects.all().order_by("name")
        context["title"] = obj.name
        context["title_bar"] = _("Kafedralar")     
        return context
    