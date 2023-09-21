from datetime import datetime
from main.models.posts import Navbar

def global_variables(request):
    context = {
        "today": datetime.now(),
        "navbar": Navbar.objects.filter(status="base", visible=True).order_by("order_num")
    }
    return context