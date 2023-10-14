from django.urls import path

from .posts.view import StudyProgramView

urlpatterns = [
    path("posts/study_programs", StudyProgramView.as_view(), name="")    
]
