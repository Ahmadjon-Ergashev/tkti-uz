import random
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from main.models import news


# django admin actions
@admin.action(description=_("clone post"))
def duplicate(modeladmin, request, queryset):
    for i in queryset:
        i.pk = None
        i.slug += str(random.randint(111111, 999999))
        i.save()


@admin.register(news.News)
class NewsAdmin(admin.ModelAdmin):
    actions = (duplicate, )
    ordering = ("-added_at", )
    date_hierarchy = "added_at"
    search_fields = ("title", )
    filter_horizontal = ["hashtag"]
    list_display_links = ("title", )
    list_filter = ("category", "status", "added_at")
    list_editable = ("post_viewed_count", "category", "status")
    list_display = ("id", "title", "post_viewed_count", "category", "status", "added_at")
    readonly_fields = ("author", "update_user", "updated_at", "get_image_file")

    fieldsets = (
        (_("Umumiy o'zgaruvchilar"), {
            "classes": ("extrapretty"),
            "fields": (
                "category", "status",
                "added_at", "author_post", "hashtag"          
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
                "title", "post"                
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


@admin.register(news.Ads)
class AdsAdmin(admin.ModelAdmin):
    actions = (duplicate, )
    ordering = ("-added_at", )
    date_hierarchy = "added_at"
    search_fields = ("title", )
    filter_horizontal = ["hashtag"]
    list_display_links = ("title", )
    list_filter = ("status", "added_at")
    list_editable = ("post_viewed_count", "status")
    list_display = ("id", "title", "post_viewed_count", "status", "added_at")
    readonly_fields = ("author", "update_user", "updated_at", "get_image_file")

    fieldsets = (
        (_("Umumiy o'zgaruvchilar"), {
            "classes": ("extrapretty"),
            "fields": (
                "status",
                "added_at", "author_post", "hashtag"
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
                "title", "post"                
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
    get_image_file.short_description = _("E'lonlar uchun tanlangan rasmli fayl")

    def save_model(self, request, obj, form, change):
        if obj.author:
            obj.update_user = request.user
        else:
            obj.auhtor = request.user
        return super().save_model(request, obj, form, change)
    
    def get_prepopulated_fields(self, request, obj):
        return {"slug": ("title", )}
    

@admin.register(news.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_editable = ("order_num", )
    list_display = ("name", "order_num", "added_at")

    fieldsets = (
        (None, {
            'fields': (
                "name", "order_num"
            ),
        }),
    )


@admin.register(news.VideoGallery)
class VideoGallyadmin(admin.ModelAdmin):
    actions = [duplicate]
    list_editable = ("status", )
    list_display_links = ("id", "title")
    prepopulated_fields = ({"slug": ("title", )})
    list_display = ("id", "title", "status", "added_at")
    readonly_fields = ["author", "post_viewed_count", "update_at"]

    fieldsets = (
        (None, {
            "fields": (
                "title", "added_at", "poster", "video_file", "status"
            ),
        }),
        
        (_("Automatik to'ldiriladigan fieldlar"), {
            "classes": ("collapse", ),
            "fields": (
                "author", "post_viewed_count", "slug", "update_at"
            ),
        }),
    )
    