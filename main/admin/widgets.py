from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from main.models.widgets import SocialNetworks


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