import random
from django.db.models import Q
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from main.models import news
from main.models import posts


# django admin actions
@admin.action(description=_("Nusxa ko'chirish"))
def duplicate(modeladmin, request, queryset):
    for i in queryset:
        i.pk = None
        i.slug += str(random.randint(111111, 999999)) 
        i.save()


@admin.register(news.News)
class NewsAdmin(admin.ModelAdmin):
    actions = (duplicate, )
    list_per_page = 10
    ordering = ("-added_at", )
    date_hierarchy = "added_at"
    list_editable = ("status", )
    list_display_links = ("title_uz", )
    list_filter = ("status", "added_at")
    search_fields = ("title_uz", "title_en", "title_ru")
    readonly_fields = ("author", "update_user", "updated_at", "get_image_file")
    list_display = ("id", "title_uz", "post_viewed_count", "status", "added_at")
    filter_horizontal = ["hashtag", "faculty_dact", "departments", "section_and_centers", "brm"]

    fieldsets = (
        (_("Umumiy o'zgaruvchilar"), {
            "classes": ("extrapretty", ),
            "fields": (
                "status",
                "added_at", "author_post", "hashtag"          
            ),
        }),
        (_("Aloqadorlar"), {
            "classes": ("collapse", ),
            "fields": (
                "faculty_dact",       
                "departments",
                "section_and_centers",
                "brm",
            ),
        }),
        (_("Media fayllar"), {
            "classes": ("collapse", ),
            "fields": (
                ("image", "get_image_file"),
                ("video_file", ),
                ("pdf_file", "pdf_file_en", "pdf_file_ru")
            ),
        }),
        (_("O'zbek tilida"), {
            "fields": (
                "title_uz", "post_uz"                
            ),
        }),
        (_("Rus tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_ru", "post_ru"                
            ),
        }),
        (_("Ingiliz tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_en", "post_en"                
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

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "faculty_dact":
            try:
                posts_list = posts.Posts.objects.filter(
                    Q(faculty=True) | Q(navbar__slug="doktorantura") |
                    Q(navbar__slug="doktorantura-qabul")
                ).select_related("author", "update_user", "navbar")
                kwargs["queryset"] = posts_list
            except Exception as e:
                kwargs["queryset"] = posts.Posts.objects.none()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_image_file(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' alt='asosiy rasm' width=100/>")
    get_image_file.short_description = _("Yangilik uchun tanlangan rasmli fayl")

    def save_model(self, request, obj, form, change):
        if obj.author:
            obj.update_user = request.user
        else:
            obj.author = request.user
        return super().save_model(request, obj, form, change)
    
    def get_prepopulated_fields(self, request, obj):
        return {"slug": ("title_uz", )}

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related(
            "author", "update_user").prefetch_related(
            "faculty_dact", "departments", "section_and_centers",
            "hashtag", "brm")
        return qs


@admin.register(news.Ads)
class AdsAdmin(admin.ModelAdmin):
    actions = (duplicate, )
    list_per_page = 10
    ordering = ("-added_at", )
    date_hierarchy = "added_at"
    filter_horizontal = ["hashtag"]
    list_display_links = ("title_uz", )
    list_filter = ("status", "added_at")
    list_editable = ("post_viewed_count", "status")
    search_fields = ("title_uz", "title_en", "title_ru")
    readonly_fields = ("author", "update_user", "updated_at", "get_image_file")
    list_display = ("id", "title_uz", "post_viewed_count", "status", "added_at")

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
                ("video_file", ),
                ("pdf_file", "pdf_file_en", "pdf_file_ru")
            ),
        }),
        (_("O'zbek tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_uz", "post_uz"                
            ),
        }),
        (_("Rus tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_ru", "post_ru"                
            ),
        }),
        (_("Ingiliz tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_en", "post_en"                
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
            obj.author = request.user
        return super().save_model(request, obj, form, change)
    
    def get_prepopulated_fields(self, request, obj):
        return {"slug": ("title_uz", )}


@admin.register(news.Events)
class EventsAdmin(admin.ModelAdmin):
    actions = (duplicate, )
    list_per_page = 10
    ordering = ("-added_at", )
    date_hierarchy = "added_at"
    list_display_links = ("title_uz", )
    list_editable = ("post_viewed_count", "status")
    list_filter = ("status", "added_at", "event_type")
    search_fields = ("title_uz", "title_en", "title_ru")
    readonly_fields = ("author", "update_user", "updated_at", "get_image_file")
    list_display = ("id", "title_uz", "event_type", "post_viewed_count", "status", "added_at")

    fieldsets = (
        (_("Umumiy o'zgaruvchilar"), {
            "classes": ("extrapretty", ),
            "fields": (
                "status", "event_type", "phone", 
                "added_at", "author_post", "extra_phone"
            ),
        }),
        (_("Media fayllar"), {
            "fields": (
                ("image", "get_image_file"),
                ("video_file",),
                ("pdf_file", "pdf_file_en", "pdf_file_ru")
            ),
        }),
        (_("O'zbek tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_uz", "post_uz", "location_uz"                
            ),
        }),
        (_("Rus tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_ru", "post_ru", "location_ru"              
            ),
        }),
        (_("Ingiliz tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_en", "post_en", "location_en"     
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
    get_image_file.short_description = _("Tadbir uchun tanlangan rasmli fayl")

    def save_model(self, request, obj, form, change):
        if obj.author:
            obj.update_user = request.user
        else:
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def get_prepopulated_fields(self, request, obj):
        return {"slug": ("title_uz", )}


@admin.register(news.VideoGallery)
class VideoGallyadmin(admin.ModelAdmin):
    actions = [duplicate]
    list_per_page = 10
    list_editable = ("status", )
    list_display_links = ("id", "title_uz")
    prepopulated_fields = ({"slug": ("title_uz", )})
    list_display = ("id", "title_uz", "status", "added_at")
    readonly_fields = ["author", "post_viewed_count", "update_at"]

    fieldsets = (
        (None, {
            "fields": (
                ("title_uz", "title_en", "title_ru"), 
                "added_at", "poster", "status", "post",
            ),
        }),
        
        (_("Automatik to'ldiriladigan fieldlar"), {
            "classes": ("collapse", ),
            "fields": (
                "author", "post_viewed_count", "slug", "update_at"
            ),
        }),
    )


@admin.register(news.PhotoGallary)
class PhotoGallary(admin.ModelAdmin):
    list_per_page = 5
    readonly_fields = ("get_image", )
    list_display_links = ("id", "get_image")
    list_display = ("id", "image", "news", "get_image")

    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width=250 />")

    