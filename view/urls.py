from django.urls import path

# local vars
from view.news import views as news
from view.posts import views as posts
from view.widgets import views as widgets


posts = [
    path("", posts.Home, name="home"),
    path("posts/navbar/<slug:navbar_slug>/", posts.PostsListView.as_view(), name="posts_nav"),
    path("posts/sections/<slug:post_slug>/", posts.SectionsDetailView.as_view(), name="sect_nav"),
    path("posts/navbar/post/<slug:post_slug>/", posts.PostDetailView.as_view(), name="post_detail"),
    path("posts/departments/<slug:dept_slug>/", posts.DepartmentsDetailView.as_view(), name="dept_detail")
]
news = [
    path("upload/images/", news.Upload_Images),
    path("ads/", news.AdsView.as_view(), name="ads"),
    path("news/", news.NewsView.as_view(), name="news"),
    path("videos/", news.VideoView.as_view(), name="videos"),
    path("photo/gallary/", news.PhotoGallaryView.as_view(), name="photo_gallary"),
    path("ads/detail/<slug:obj_slug>/", news.AdsDetailView.as_view(), name="ads_detail"),
    path("news/detail/<slug:obj_slug>/", news.NewsDetailView.as_view(), name="news_detail"),
    path("videos/detail/<slug:obj_slug>/", news.VideosDetailView.as_view(), name="video_detail"),
]
widgets = [
    path("faq", widgets.FaqView.as_view(), name="faq"),
    path("flag", widgets.FlagView.as_view(), name="flag"),
    path("anthem", widgets.AnthemView.as_view(), name="anthem"),
    path("sitemap", widgets.SiteMapView.as_view(), name="site_map"),
    path("coat_of_arms", widgets.CoatofArmsView.as_view(), name="coat_of_arms"),
]

urlpatterns = [] + posts + news + widgets
