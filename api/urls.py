from django.urls import path
from rest_framework.routers import DefaultRouter

from api.posts import view as posts
from api.widgets import view as widgets

router = DefaultRouter()
router.register("posts/faculty_list", posts.FacultyView)
router.register("posts/study_programs", posts.StudyProgramView)
router.register("posts/departments_list", posts.DepartmentsView)


widgets = [
    path("widgets/years", widgets.YearView.as_view(), name="years_list")
]

urlpatterns = [] + widgets + router.urls
