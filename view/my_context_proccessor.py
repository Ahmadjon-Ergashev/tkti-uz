from datetime import datetime
from django.utils.translation import gettext_lazy as _

# local
from main.models.posts import Navbar
from main.models.widgets import SocialNetworks


def global_variables(request):
    context = {
        "today": datetime.now(),
        "navbar": Navbar.objects.filter(status="base", visible=True).order_by("order_num"),
        "social_networks": SocialNetworks.objects.all().order_by("order_num"),
        "news_tab": _("Yangiliklar"),
        "ads_tab": _("E'lonlar"),
        "latest": _("Eng so'ngi")
    }
    return context