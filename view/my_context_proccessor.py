from datetime import datetime


def global_variables(request):
    context = {
        "today": datetime.now() 
    }
    return context