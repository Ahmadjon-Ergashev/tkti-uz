from django.urls import path

import view.searching.views as views


urlpatterns = [
    path("ads/list/<str:query>", views.SearchingAdsNewsView.as_view()),
    path("news/list/<str:query>", views.SearchingListNewsView.as_view()),
    path("posts/list/<str:query>", views.SearchingPostsNewsView.as_view()),
    path("events/list/<str:query>", views.SearchingEventsNewsView.as_view()),
]
