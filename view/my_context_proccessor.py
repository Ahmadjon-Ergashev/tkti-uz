import random
from datetime import datetime
from django.utils import timezone
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.db.models import ExpressionWrapper, F, DateTimeField

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
            cache.set("navbar", navbar_list, 60 * 30)
    except Exception as e:
        print(e)
    current_time = timezone.now()
    event = news.Events.objects.select_related("event_type").filter(
        status="pub", added_at__gte=current_time
    ).annotate(
        time_diff=ExpressionWrapper(
            F('added_at') - current_time,
            output_field=DateTimeField()
        )
    ).order_by('time_diff')
    if event.exists():
        random_one = random.choice(event)
        if random_one:
            coming_time_delta = random_one.added_at - timezone.now()
            days_until_event_starts = coming_time_delta.days
            if days_until_event_starts == 0:
                start_time = _("Bugun")
            else:
                word = _("kun qoldi")
                start_time = f"{days_until_event_starts} {word}"
        else:
            start_time = "No upcoming event"
    else:
        random_one = None
        start_time = "No upcoming event"

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

    context = {
        "navbar": posts.Navbar.objects.filter(status="base", visible=True).order_by("order_num").only(
            "name", "slug", "id"
        ).prefetch_related("children"),
        "quick_links": widgets.QuickLinks.objects.order_by("order_num").only(
            "url", "name"
        ),
        "last_news": news.News.objects.filter(status="pub").order_by("-added_at")[:20],
        "base_variables": widgets.BaseVariables.objects.last(),
        "top_navbar": widgets.TopNavbar.objects.only("name", "url").order_by("order_num"),
        "upcoming_event_first": random_one,
        "start_time": start_time,
        "start_time_title": _("Boshlanish vaqtigacha "),
        # text variables
        "next": _("oldinga"),
        "about": _("Haqida"),
        "previous": _("ortga"),
        "target": _("Maqsadi"),
        "home": _("Bosh sahifa"),
        "ads_tab": _("E'lonlar"),
        "workers": _("Ma'muriyat"),
        "activity": _("Faoliyat"),
        "latest": _("Eng so'ngi"),
        "read_more": _("Batafsil"),
        "download": _("Ko'rish"),
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
        "zip_file_title": _("Mavzuga aloqador qo'shimcha faylarni yuklab olish"),
        "zip_file_title_2": _("Mavzuga aloqador qo'shimcha faylar"),
        "download_2": _("Yuklab olish"),
        "activity_docs": _("Faoliyat hujjatlari"),
        "about_section": _("Bo'lim haqida"),
        "about_department": _("Kafedra haqida"),
    }
    try:
        name = str(context["base_variables"].name).split(maxsplit=2)
        context["web_name"] = name
    except Exception as e:
        print(e)
    if navbar is None:
        navbar = {}
    return context | translate_words | navbar
