from django.urls import path

# local vars
from view.posts.views import Home


urlpatterns = [
    path("", Home, name="home")
]
