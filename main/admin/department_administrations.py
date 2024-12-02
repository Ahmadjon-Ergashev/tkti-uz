from django.contrib import admin

import main.models as models


@admin.register(models.DepartmentHeadAdministrations)
class DepartmentHeadAdministrationsAdmin(admin.ModelAdmin):
    list_filter = ("department",)
    list_editable = ("department",)
    search_fields = ("id", "f_name", "phone")
    list_display_links = ("id", "f_name", "phone")
    list_display = ("id", "f_name", "phone", "department")


@admin.register(models.DepartmentAdministrationsPositions)
class DepartmentAdministrationsPositionsAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_editable = ("order_num",)
    list_display_links = ("id", "name")
    list_display = ("id", "name", "order_num")


@admin.register(models.DepartmentAdministrationsNew)
class DepartmentAdministrationsNew(admin.ModelAdmin):
    search_fields = ("id", "f_name")
    list_display_links = ("id", "f_name")
    list_filter = ("position", "department")
    list_editable = ("position", "department")
    list_display = ("id", "f_name", "position", "department")
