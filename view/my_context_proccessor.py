from datetime import datetime
from main.models.posts import Navbar
from main.models.widgets import SocialNetworks

def global_variables(request):
    context = {
        "today": datetime.now(),
        "navbar": Navbar.objects.filter(status="base", visible=True).order_by("order_num"),
        "social_networks": SocialNetworks.objects.all().order_by("order_num") 
    }
    return context