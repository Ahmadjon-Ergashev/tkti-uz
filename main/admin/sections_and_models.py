import random
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

import main.models as models


@admin.action(description=_("Nusxa ko'chirish"))
def duplicate(modeladmin, request, queryset):
    for i in queryset:
        i.pk = None
        i.slug += str(random.randint(1111, 9999))
        i.save()


@admin.action(description=_("Nusxa ko'chirish"))
def clone(modeladmin, request, queryset):
    for i in queryset:
        i.pk = None
        i.f_name += " - copy"
        i.save()


@admin.register(models.Workers)
class WorkersAdmin(admin.ModelAdmin):
    actions = [clone]
    list_per_page = 10
    list_filter = ("section",)
    list_editable = ("order_num",)
    readonly_fields = ["get_image"]
    list_display_links = ("f_name_uz",)
    search_fields = ("f_name_uz", "f_name_ru", "f_name_en")
    list_display = ("id", "f_name_uz", "section", "order_num", "self_position", "added_at")

    fieldsets = (
        (None, {
            "fields": (
                "position", "self_position", "section",
                "phone", "extra_phone", "email", "order_num",
                ("image", "get_image")
            ),
        }),
        (_("O'zbek tilida"), {
            'classes': ('collapse',),
            "fields": (
                "f_name_uz",
            ),
        }),
        (_("Rus tilida"), {
            'classes': ('collapse',),
            "fields": (
                "f_name_ru",
            ),
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse',),
            "fields": (
                "f_name_en",
            ),
        }),
    )

    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width='250' />")

    get_image.short_description = _("Tanlangan rasm")


@admin.register(models.SectionsAndCenters)
class SectionsAdmin(admin.ModelAdmin):
    actions = [duplicate]
    list_per_page = 10
    list_display_links = ("title_uz",)
    list_display = ("id", "title_uz", "added_at")
    prepopulated_fields = ({"slug": ("title_uz",)})
    search_fields = ("title_uz", "title_ru", "title_en")

    fieldsets = (
        (None, {
            "fields": (
                "navbar", "image", "zip_file"
            ),
        }),
        (_("O'zbek tilida"), {
            'classes': ('collapse',),
            "fields": (
                "title_uz", "about_uz", "target_uz", "activity_uz", "pdf_file"
            ),
        }),
        (_("Rus tilida"), {
            'classes': ('collapse',),
            "fields": (
                "title_ru", "about_ru", "target_ru", "activity_ru", "pdf_file_ru"
            ),
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse',),
            "fields": (
                "title_en", "about_en", "target_en", "activity_en", "pdf_file_en"
            ),
        }),
        (_("Automatik to'ldiriladigan fieldlar"), {
            'classes': ('collapse',),
            "fields": (
                "slug",
            ),
        }),
    )
