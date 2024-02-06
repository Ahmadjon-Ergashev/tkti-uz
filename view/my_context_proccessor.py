from datetime import datetime
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

# local
from main.models import (
    posts, widgets, news
)


def global_variables(request):
    navbar = {}
    try:
        navbar = cache.get("navbar")
        if not navbar:
            navbar_list = {
                "today": datetime.now(),
                "social_networks": widgets.SocialNetworks.objects.order_by("order_num").only(
                    "name", "color", "url", "icon"
                ),
            }
            cache.set("navbar", navbar_list, 60*30)
    except Exception as e:
        print(e)
    context = {
        "navbar": posts.Navbar.objects.filter(status="base", visible=True).order_by("order_num").only(
            "name", "slug", "id"
        ).prefetch_related("children"),
        "quick_links": widgets.QuickLinks.objects.order_by("order_num").only(
            "url", "name"
        ),
        "last_news": news.News.objects.filter(status="pub").order_by("-added_at")[:20],

        # text variables
        "next": _("oldinga"),
        "about": _("Xaqida"),
        "previous": _("ortga"),
        "target": _("Maqsadi"),
        "home": _("Bosh sahifa"),
        "ads_tab": _("E'lonlar"),
        "workers": _("Xodimlar"),
        "activity": _("Faoliyati"),
        "latest": _("Eng so'ngi"),
        "read_more": _("Batafsil"),
        "download": _("Yuklab olish"),
        "news_tab": _("Yangiliklar"),
        "email_title": _("E-Pochta"),
        "address_title": _("Manzil"),
        "document_name": _("Hujjat nomi"),
        "all_images": _("Barcha rasmlar"),
        "phone_title": _("Telefon raqam"),
        "contact_edu_area": _("Bog'lanish"),
        "money_priz": _("Moliyaviy imtiyoz"),
        "photo_grid_title": _("Foto lavhalar"),
        "quick_link_title": _("Tezkor havolalar"),
        "social_networks_title": _("Ijtimoiy tarmoqlar"),
        "extra_phone_title": _("Qo'shimcha Telefon raqam"),
    }
    translate_words = {
        "arxiv": _("Arxiv"),
        "all": _("Barchasi"),
        "search": _("Qidirish"),
        "events": _("Voqealar"),
        "title": _("Bosh sahifa"),
        "faculty_title": _("Fakultetlar"),
        "sp_faculty": _("Sohani tanlang"),
        "ads_section_title": _("E'lonlar"),
        "sp_way": _("Yo'nalishni tanlang"),
        "sp_type": _("Ta'lim turini tanlang"),
        "videos_section_title": _("Videolar"),
        "the_most_read": _("Top yangiliklar"),
        "upcoming": _("Yaqinlashib kelayotganlar"),
        "nth_faculty": _("tarkibidagi kafedralar"),
        "usuful_links_title": _("Foydali havolalar"),
        "the_last_news": _("Eng so'ngi yangiliklar"),
        "study_way_title": _("Ta'lim dasturi katalogi"),
        "talented_student_title": _("Iqtidorli talabalar"),
        "not_found_404": _("Afsuski hechqanday ma'lumot topilmadi :("),
    }
    if navbar is None:
        navbar = {}
    return context | translate_words | navbar
