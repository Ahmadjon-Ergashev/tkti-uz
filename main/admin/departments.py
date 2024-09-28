import random
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

import main.models as models


# django admin actions
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


class DepartmentCharterDocumentAdmin(admin.TabularInline):
    model = models.DepartmentCharterDocument
    extra = 1


class DepartmentPlanDocumentAdmin(admin.TabularInline):
    model = models.DepartmentPlanDocument
    extra = 1


@admin.register(models.Departments)
class DepartmentsAdmin(admin.ModelAdmin):
    actions = [duplicate]
    list_per_page = 10
    search_fields = ("name_uz",)
    list_editable = ("faculty",)
    list_display_links = ("name_uz",)
    list_display = ("id", "name_uz", "faculty")
    readonly_fields = ("added_at", "post_viewed_count")
    inlines = [DepartmentCharterDocumentAdmin, DepartmentPlanDocumentAdmin]

    fieldsets = (
        (None, {
            "fields": (
                "faculty",
                ("pdf_file", "pdf_file_en", "pdf_file_ru", "zip_file")
            ),
        }),
        (_("O'zbek tilida ma'lumotlar"), {
            'classes': ('collapse',),
            "fields": (
                "name_uz", "about_uz", "target_uz", "activity_uz"
            ),
        }),
        (_("Rus tilida ma'lumotlar"), {
            'classes': ('collapse',),
            "fields": (
                "name_ru", "about_ru", "target_ru", "activity_ru"
            ),
        }),
        (_("Ingiliz tilida ma'lumotlar"), {
            'classes': ('collapse',),
            "fields": (
                "name_en", "about_en", "target_en", "activity_en"
            ),
        }),
        (_("Automatik to'ldiriladigan bo'limlar"), {
            'classes': ('collapse',),
            "fields": (
                "slug", "added_at", "post_viewed_count"
            )
        })
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "faculty":
            try:
                kwargs["queryset"] = models.Posts.objects.filter(faculty=True)
            except Exception as e:
                kwargs["queryset"] = models.Posts.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_prepopulated_fields(self, request, obj):
        return {"slug": ("name_uz",)}


@admin.register(models.DepartmentsAdmistrations)
class DeptAdminstraAdmin(admin.ModelAdmin):
    actions = [clone]
    list_per_page = 10
    search_fields = ("f_name_uz",)
    list_editable = ("order_num",)
    list_display_links = ("f_name_uz",)
    autocomplete_fields = ("department",)
    readonly_fields = ("get_image", "added_at", "updated_at",)
    list_display = ("id", "f_name_uz", "department", "order_num", "added_at")

    fieldsets = (
        (None, {
            "fields": (
                "department", ("image", "get_image"),
                "phone_number", "email"
            ),
        }),
        (_("O'zbek tilida ma'lumotlar"), {
            'classes': ('collapse',),
            "fields": (
                "f_name_uz", "job_name_uz", "admission_day_uz"
            ),
        }),
        (_("Rus tilida ma'lumotlar"), {
            'classes': ('collapse',),
            "fields": (
                "f_name_ru", "job_name_ru", "admission_day_ru"
            ),
        }),
        (_("Ingiliz tilida ma'lumotlar"), {
            'classes': ('collapse',),
            "fields": (
                "f_name_en", "job_name_en", "admission_day_en"
            ),
        }),
        (_("Automatik to'ldiriladigan bo'limlar"), {
            'classes': ('collapse',),
            "fields": (
                "added_at", "updated_at"
            )
        })
    )

    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width='250' />")

    get_image.short_description = _("Tanlangan rasm")
