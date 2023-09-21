import random
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from main.models.posts import Navbar, Posts
from guardian.admin import GuardedModelAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


# django admin actions
@admin.action(description="clone post")
def duplicate(modeladmin, request, queryset):
    for i in queryset:
        i.pk = None
        i.slug += str(random.randint(9999, 9999))
        i.save()


@admin.register(Navbar)
class NavbarAdmin(MPTTModelAdmin):
    """ Admin view for Navigation bar model """
    ordering = ("name", )
    search_fields = ("name", )
    date_hierarchy = "added_at"
    list_display_links = ("name", )
    list_editable = ("order_num", "status", "inside_order_num")
    list_filter = ("parent", "added_at", "status", "visible", "author")
    readonly_fields = ("author", "added_at", "update_user", "updated_at")
    list_display = ("id", "name", "parent", "status", "order_num", "inside_order_num", "visible", "added_at")

    fieldsets = (
        (_("Nomi"), {
            "classes": ("extrapretty"),
            "fields": (
                "name",             
            ),
        }),
        (_("Umumiy o'zgaruvchilar"), {
            "classes": ("extrapretty"),
            "fields": (
                "parent",
                "status", 
                "order_num", 
                "inside_order_num", 
                "visible",                
            ),
        }),
        (_("Automatik to'ldiriladigan fieldlar"), {
            "classes": ("collapse", ),
            "fields": (
                "author",
                "slug",
                "added_at",
                "update_user",
                "updated_at"
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.author:
            obj.update_user = request.user
        else:
            obj.auhtor = request.user
        return super().save_model(request, obj, form, change)
    
    def get_prepopulated_fields(self, request, obj):
        return {"slug": ("name", )}



@admin.register(Posts)
class PostsAdmin(GuardedModelAdmin):
    """ Admin view for Posts """
    ordering = ("-added_at", )
    actions = (duplicate, )
    date_hierarchy = "added_at"
    empty_value_display = "Tanlanmagan"
    search_fields = ("title", "navbar__name")
    list_filter = ("navbar", "status", "author", "added_at")
    readonly_fields = ("author", "update_user", "updated_at", "get_image_file")
    list_display = ("id", "title", "navbar", "status", "post_viewed_count", "author", "added_at", "updated_at")

    fieldsets = (
        (_("Umumiy o'zgaruvchilar"), {
            "classes": ("extrapretty"),
            "fields": (
                "navbar", "status",
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
    get_image_file.short_description = _("Post uchun tanlangan rasmli fayl")

    def save_model(self, request, obj, form, change):
        if obj.author:
            obj.update_user = request.user
        else:
            obj.auhtor = request.user
        return super().save_model(request, obj, form, change)
    
    def get_prepopulated_fields(self, request, obj):
        return {"slug": ("title", )}
