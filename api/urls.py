from django.urls import path

from api.posts import view as posts
from api.widgets import view as widgets


posts = [
    path("posts/faculty_list", posts.FacultyView.as_view(), name="faculty_list"),    
    path("posts/departments_list", posts.DepartmentsView.as_view(), name="dept_list"),    
    path("posts/study_programs", posts.StudyProgramView.as_view(), name="study_pogram"),    
]

widgets = [
    path("widgets/years", widgets.YearView.as_view(), name="years_list")
]

urlpatterns = [] + posts + widgets
