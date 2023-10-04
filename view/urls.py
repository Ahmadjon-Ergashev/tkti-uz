from django.urls import path

# local vars
from view.posts.views import (
    Home, PostsListView, PostDetailView
)
from view.news.views import (
    NewsDetailView, 
)

posts = [
    path("posts/navbar/<slug:navbar_slug>/", PostsListView.as_view(), name="posts_nav"),
    path("posts/navbar/post/<slug:post_slug>/", PostDetailView.as_view(), name="post_detail"),
]
news = [
    path("news/detail/<slug:obj_slug>/", NewsDetailView.as_view(), name="news_detail")
]

urlpatterns = [
    path("", Home, name="home")
]
urlpatterns += posts + news
