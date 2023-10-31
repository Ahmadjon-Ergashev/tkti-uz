from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _

# local
from main.models import posts, widgets


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
    
