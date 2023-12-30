from datetime import datetime
from django.utils.translation import gettext_lazy as _

# local
from main.models import (
    posts, widgets, news
)


def global_variables(request):
    context = {
        "today": datetime.now(),
        "quick_links": widgets.QuickLinks.objects.all().order_by("order_num").only(
            "url", "name"
        ),
        "social_networks": widgets.SocialNetworks.objects.all().order_by("order_num").only(
            "name", "color", "url", "icon"
        ),
        "last_news": news.News.objects.filter(status="pub").order_by("-added_at")[:20],
        "most_read_ads": news.Ads.objects.filter(status="pub").order_by("-post_viewed_count")[:4].only(
            "title", "added_at", "post_viewed_count", "slug",
        ),
        "most_read_news": news.News.objects.filter(status="pub").order_by("-post_viewed_count")[:4].only(
            "title", "added_at", "post_viewed_count", "slug",
        ),
        "navbar": posts.Navbar.objects.filter(status="base", visible=True).order_by("order_num").only(
            "name", "slug", "id"
        ).prefetch_related("children"),

        # text variables
        "next": _("oldinga"),
        "about": _("Xaqida"),
        "previous": _("ortga"),
        "target": _("Maqsadi"),
        "home": _("Bosh sahifa"),
        "ads_tab": _("E'lonlar"),
        "workers": _("Xodimlar"),
        "activity": _("Faoliyati"),
        "latest" : _("Eng so'ngi"),
        "read_more": _("Batafsil"),
        "news_tab": _("Yangiliklar"),
        "email_title": _("E-Pochta"),
        "address_title" : _("Manzil"),
        "all_images": _("Barcha rasmlar"),
        "phone_title" : _("Telefon raqam"),
        "contact_edu_area": _("Bog'lanish"),
        "money_priz" : _("Moliyaviy imtiyoz"),
        "photo_grid_title": _("Foto lavhalar"),
        "quick_link_title": _("Tezkor havolalar"),
        "social_networks_title": _("Ijtimoiy tarmoqlar"),
        "extra_phone_title" : _("Qo'shimcha Telefon raqam"),
    }
    return context