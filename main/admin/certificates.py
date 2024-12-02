import random
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

import main.models as models


@admin.action(description=_("Nusxa ko'chirish"))
def duplicate(modeladmin, request, queryset):
    for i in queryset:
        i.pk = None
        i.save()


@admin.register(models.CertificatesThemes)
class CertificatesThemeAdmin(admin.ModelAdmin):
    actions = [duplicate]
    search_fields = ("name", )
    list_display = ("id", "name", )
    list_display_links = ("id", "name", )


@admin.register(models.Certificates)
class CertificatesAdmin(admin.ModelAdmin):
    actions = [duplicate]
    search_fields = ("f_name", )
    list_filter = ("theme", "year")
    list_editable = ("year", "theme")
    list_display_links = ("id", "f_name", )
    list_display = ("id", "f_name", "year", "theme", "add_time")
