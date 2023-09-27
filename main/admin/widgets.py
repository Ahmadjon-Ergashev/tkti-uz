from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from django.utils.safestring import mark_safe

from main.models.widgets import (
    SocialNetworks, HeaderIMG, UsefullLinks, QuickLinks, Statistika
)


@admin.register(SocialNetworks)
class SocialNetworkingAdmin(GuardedModelAdmin):
    search_fields = ("name", )
    ordering = ("-added_at", )
    list_display_links = ("name", )
    list_editable = ("order_num", "color")
    list_display = ("id", "name", "order_num", "color", "added_at")

    def save_model(self, request, obj, form, change):
        if obj.author:
            obj.update_user = request.user
        else:
            obj.auhtor = request.user
        return super().save_model(request, obj, form, change)
    

@admin.register(HeaderIMG)
class HeaderIMGAdmin(GuardedModelAdmin):
    list_editable = ("order_num", )
    readonly_fields = ["get_image"]
    list_display_links = ("get_image", )
    list_display = ("id", "get_image", "order_num", "add_time")

    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width=100 />")
    

@admin.register(UsefullLinks)
class LinksAdmin(GuardedModelAdmin):
    search_fields = ("name", )
    list_display_links = ("name", )
    readonly_fields = ("get_logo", )
    list_display = ("id", "name", "get_logo", "add_time")

    def get_logo(self, obj):
        return mark_safe(f"<img src='{obj.logo.url}' width=100 />")
    

@admin.register(QuickLinks)
class QuickLinksAdmin(admin.ModelAdmin):
    ordering = ("-added_at", )
    list_display_links = ("name", )
    list_editable = ("order_num", "url")
    list_display = ("id", "name", "order_num", "url", "added_at")
    

@admin.register(Statistika)
class StatistikaAdmin(admin.ModelAdmin):
    ordering = ("-added_at", )
    list_display_links = ("name", )
    list_editable = ("order_num", "quantity")
    list_display = ("id", "name", "quantity", "order_num", "added_at")