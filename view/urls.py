from django.urls import path

# local vars
from view.posts.views import (
    Home, PostsListView, PostDetailView
)


posts = [
    path("posts/navbar/<slug:navbar_slug>/", PostsListView.as_view(), name="posts_nav"),
    path("posts/navbar/post/<slug:post_slug>/", PostDetailView.as_view(), name="post_detail"),
]

urlpatterns = [
    path("", Home, name="home")
]
urlpatterns += posts
