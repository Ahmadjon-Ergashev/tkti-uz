from django.urls import path

import view.partners.view as view

urlpatterns = [
	path("list/", view.PartnersView.as_view(), name="partners_list")
]
