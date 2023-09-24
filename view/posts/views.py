from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404

# local models
from main.models.posts import (
    Posts, Status, Navbar
)
from main.models.widgets import HeaderIMG, UsefullLinks



def Home(request):
    """ for home page view """
    context = {
        "title": _("Bosh sahifa"),
        "header_img": HeaderIMG.objects.all().order_by("order_num"),
        "usefull_links": UsefullLinks.objects.all().order_by("-add_time")
    }
    return render(request, "home.html", context)


class PostsListView(ListView):
    """ get all posts what connected to navbar """
    model = Posts
    paginate_by = 15
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
        try:
            context["category_list"] = Navbar.objects.filter(parent_id=navbar_name.parent.id)
        except AttributeError:
            context["category_list"] = navbar_name.get_children()
        context["read_more"] = _("Batafsil")
        context["home"] = _("Asosiy sahifa")
        context["empty"] = _("Afsuski hozircha ma'lumotlar topilmadi :(")
        return context


class PostDetailView(DetailView):
    """ get detail of posts """
    model = Posts
    template_name = "pages/posts/post_detail.html"

    def get_object(self, queryset=None):
        """Override the get_object method to customize the object retrieval."""
        post_slug = self.kwargs["post_slug"]
        obj = get_object_or_404(Posts, slug=post_slug)
        return obj
    