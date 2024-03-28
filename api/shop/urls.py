from rest_framework.routers import DefaultRouter

import api.shop.view as views

router = DefaultRouter()
router.register("list", views.ShopView)
router.register("category/list", views.ShopCategoryView)

urlpatterns = [] + router.urls

