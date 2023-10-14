import random
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from guardian.admin import GuardedModelAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


from main.models.posts import (
    Navbar, Posts, FacultyAdministration, Departments, StudyProgram
)


# django admin actions
@admin.action(description=_("Nusxa ko'chirish"))
def duplicate(modeladmin, request, queryset):
    for i in queryset:
        i.pk = None
        i.slug += str(random.randint(9999, 9999))
        i.save()

@admin.action(description=_("Nusxa ko'chirish"))
def clone(modeladmin, request, queryset):
    for i in queryset:
        i.pk = None
        i.f_name += " - copy"
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
    list_editable = ("status", )
    list_display_links = ("title", )
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


@admin.register(FacultyAdministration)
class FacultyAdmistrationAdmin(GuardedModelAdmin):
    actions = [clone]
    ordering = ("order_num", )
    list_filter = ("added_at", )
    list_editable = ("order_num", )
    list_display_links = ("f_name", )
    search_fields = ("f_name", "job_name")
    readonly_fields = ("get_image", "added_at", "updated_at")
    list_display = ("id", "f_name", "order_num", "job_name", "phone_number", "added_at")

    fieldsets = (
        (_("Umumiy ozgaruvchilar"), {
            "fields": (
              "faculty", "phone_number", "email", "order_num", ("image", "get_image")
            ),
        }),
        (_("O'zbek tilida ma'lumotlar"), {
            "fields": (
                "f_name", "job_name", "admission_day"
            ),
        }),        
        (_("Automatik to'ldiriladigan bo'limlar"), {
            'classes': ('collapse', ),
            "fields": (
                "added_at", "updated_at"
            )
        })
    )
    
    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width='250' />")
    get_image.short_description = _("Tanlangan rasm")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "faculty":
            try:
                kwargs["queryset"] = Posts.objects.filter(navbar__slug="fakultet")
            except Exception as e:
                kwargs["queryset"] = Posts.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Departments)
class DepartmentsAdmin(admin.ModelAdmin):
    list_display_links = ("name", )
    list_display = ("id", "name", "faculty")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "faculty":
            try:
                kwargs["queryset"] = Posts.objects.filter(navbar__slug="fakultet")
            except Exception as e:
                kwargs["queryset"] = Posts.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(StudyProgram)
class StudyAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("title", )
