from rest_framework.routers import DefaultRouter

from api.news import views as news
from api.posts import view as posts
from api.widgets import view as widgets


router = DefaultRouter()
router.register("ads", news.AdsView)
router.register("news", news.NewsView)
router.register("videos", news.VideoView)
router.register("widgets/years", widgets.YearView)
router.register("posts/faculty_list", posts.FacultyView)
router.register("posts/study_programs", posts.StudyProgramView)
router.register("posts/departments_list", posts.DepartmentsView)



urlpatterns = [] + router.urls
