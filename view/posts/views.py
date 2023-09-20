from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
# Create your views here.


def Home(request):
    """ for home page view """
    context = {
        "title": _("Bosh sahifa")
    }
    return render(request, "home.html", context)