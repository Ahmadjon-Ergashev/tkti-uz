import random
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from main.models.news import NewsAndAds


# django admin actions
@admin.action(description=_("clone post"))
def duplicate(modeladmin, request, queryset):
    for i in queryset:
        i.pk = None
        i.slug += str(random.randint(999999, 999999))
        i.save()


@admin.register(NewsAndAds)
class NewsAdmin(admin.ModelAdmin):
    actions = (duplicate, )
    ordering = ("-added_at", )
    date_hierarchy = "added_at"
    search_fields = ("title", )
    list_display_links = ("title", )
    list_filter = ("object_type", "status", "added_at")
    list_editable = ("post_viewed_count", "object_type", "status")
    list_display = ("id", "title", "post_viewed_count", "object_type", "status", "added_at")
    readonly_fields = ("author", "update_user", "updated_at", "get_image_file")

    fieldsets = (
        (_("Umumiy o'zgaruvchilar"), {
            "classes": ("extrapretty"),
            "fields": (
                "object_type", "status",
                "added_at", "author_post",                 
            ),
        }),
        (_("Media fayllar"), {
            "fields": (
                ("image", "get_image_file"),
                ("pdf_file", "video_file")                
            ),
        }),
        (_("O'zbek tilida"), {
            "classes": ("extrapretty"),
            "fields": (
                "title", "subtitle", "post"                
            ),
        }),
        (_("Automatik to'ldiriladigan fieldlar"), {
            "classes": ("collapse", ),
            "fields": (
                "author",
                "slug",
                "post_viewed_count",
                "update_user",
                "updated_at"
            ),
        }),
    )

    def get_image_file(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' alt='asosiy rasm' width=200/>")
    get_image_file.short_description = _("Yangilik uchun tanlangan rasmli fayl")

    def save_model(self, request, obj, form, change):
        if obj.author:
            obj.update_user = request.user
        else:
            obj.auhtor = request.user
        return super().save_model(request, obj, form, change)
    
    def get_prepopulated_fields(self, request, obj):
        return {"slug": ("title", )}