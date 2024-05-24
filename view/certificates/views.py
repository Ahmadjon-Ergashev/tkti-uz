from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

import main.models as models


class CertificatesThemesView(View):
    template_name = 'pages/posts/certificates_themes.html'

    def get(self, request, year_id):
        years_ids = models.Certificates.objects.values_list("year", flat=True).distinct()
        years = models.Year.objects.filter(id__in=years_ids).order_by("year")
        themes_ids = models.Certificates.objects.filter(year=year_id).values_list('theme', flat=True).distinct()
        themes = models.CertificatesThemes.objects.filter(id__in=themes_ids).order_by("name")
        context = {
            "years": years,
            "themes": themes,
            "year_id": year_id,
            "year_title": _("Yilni tanlang"),
            "title": _("Malaka oshirish mavzular"),
        }
        return render(request, self.template_name, context)


class CertificatesView(View):
    template_name = 'pages/posts/certificates.html'

    def get(self, request, year_id, theme_id):
        themes_ids = models.Certificates.objects.filter(year=year_id).values_list('theme', flat=True).distinct()
        themes = models.CertificatesThemes.objects.filter(id__in=themes_ids).order_by("name")
        certificates = models.Certificates.objects.filter(year=year_id, theme=theme_id).order_by("id")
        context = {
            "themes": themes,
            "year_id": year_id,
            "theme_id": theme_id,
            "certificates": certificates,
            "certificate_pdf": _("Sertifikat"),
            "title": _("Malaka oshiruvchilar ro'yhati"),
            "theme_title": _("Malaka oshirish mavzular"),
            "certificate_order": _("Sertifikat buyrug'i"),
        }
        return render(request, self.template_name, context)
