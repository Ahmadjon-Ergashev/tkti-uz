from datetime import datetime
from django.utils.translation import gettext_lazy as _

# local
from main.models.posts import Navbar
from main.models.news import NewsAndAds
from main.models.widgets import SocialNetworks, QuickLinks


def global_variables(request):
    context = {
        "today": datetime.now(),
        "quick_links": QuickLinks.objects.all().order_by("order_num"),
        "social_networks": SocialNetworks.objects.all().order_by("order_num"),
        "navbar": Navbar.objects.filter(status="base", visible=True).order_by("order_num"),
        "most_read_ads": NewsAndAds.objects.filter(object_type="ads", status="pub").order_by("-added_at")[:6],
        "most_read_news": NewsAndAds.objects.filter(object_type="news", status="pub").order_by("-added_at")[:6],

        # text variables
        "ads_tab": _("E'lonlar"),
        "latest" : _("Eng so'ngi"),
        "read_more": _("Batafsil"),
        "news_tab": _("Yangiliklar"),
        "quick_link_title": _("Tezkor havolalar"),
        "social_networks_title": _("Ijtimoiy tarmoqlar"),
    }
    return context