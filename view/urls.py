from django.urls import path

# local vars
from view.posts import views as posts
from view.news import views as news

posts = [
    path("", posts.Home, name="home"),
    path("posts/navbar/<slug:navbar_slug>/", posts.PostsListView.as_view(), name="posts_nav"),
    path("posts/navbar/post/<slug:post_slug>/", posts.PostDetailView.as_view(), name="post_detail"),
    path("posts/departments/<slug:dept_slug>/", posts.DepartmentsDetailView.as_view(), name="dept_detail"),
]
news = [
    path("news/detail/<slug:obj_slug>/", news.NewsDetailView.as_view(), name="news_detail"),
    path("upload/images/", news.Upload_Images),
]

urlpatterns = [] + posts + news
