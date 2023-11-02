from datetime import datetime
from django.utils.translation import gettext_lazy as _

# local
from main.models import (
    posts, widgets, news
)



def global_variables(request):
    context = {
        "today": datetime.now(),
        "quick_links": widgets.QuickLinks.objects.all().order_by("order_num"),
        "social_networks": widgets.SocialNetworks.objects.all().order_by("order_num"),
        "navbar": posts.Navbar.objects.filter(status="base", visible=True).order_by("order_num"),
        "most_read_ads": news.Ads.objects.filter(status="pub").order_by("-post_viewed_count")[:4].all(),
        "most_read_news": news.News.objects.filter(status="pub").order_by("-post_viewed_count")[:4].all(),

        # text variables
        "next": _("oldinga"),
        "previous": _("ortga"),
        "ads_tab": _("E'lonlar"),
        "latest" : _("Eng so'ngi"),
        "read_more": _("Batafsil"),
        "news_tab": _("Yangiliklar"),
        "photo_grid_title": _("Foto lavhalar"),
        "quick_link_title": _("Tezkor havolalar"),
        "social_networks_title": _("Ijtimoiy tarmoqlar"),
    }
    return context