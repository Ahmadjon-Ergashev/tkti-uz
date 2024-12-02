from django.urls import path

import view.certificates.views as view

urlpatterns = [
    path("themes/list/<int:year_id>", view.CertificatesThemesView.as_view(), name="theme_list"),
    path("list/<int:year_id>/<int:theme_id>", view.CertificatesView.as_view(), name="certificates_list"),
]
