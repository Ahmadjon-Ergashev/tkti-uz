from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.news import views as news
from api.posts import view as posts
from api.widgets import view as widgets


router = SimpleRouter()
router.register("ads", news.AdsView)
router.register("news", news.NewsView)
router.register("videos", news.VideoView)
router.register("news/events", news.EventView)
router.register("widgets/faq", widgets.FaqView)
router.register("widgets/years", widgets.YearView)
router.register("posts/faculty_list", posts.FacultyView)
router.register("posts/study_degree", posts.StudyDegreeView)
router.register("posts/learning_way", posts.LearningWayView)
router.register("widgets/faq_category", widgets.FaqCategoryView)
router.register("posts/adminstrations", posts.AdmistrationsView)
router.register("posts/departments_list", posts.DepartmentsView)
router.register("posts/talented_students", posts.TalentedStudentsView)


urlpatterns = [
	path("shop/", include("api.shop.urls"))
] + router.urls
