import random
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from guardian.admin import GuardedModelAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


from main.models.posts import (
    Navbar, Posts, FacultyAdministration, Departments, StudyProgram
)
from main.models import posts


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


@admin.register(posts.Navbar)
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
            obj.author = request.user
        return super().save_model(request, obj, form, change)
    
    def get_prepopulated_fields(self, request, obj):
        return {"slug": ("name", )}



@admin.register(posts.Posts)
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
                "navbar", "status", "faculty",
                "added_at", "author_post"                 
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
        if obj.navbar.slug == "fakultet":
            obj.faculty = True
        if obj.author:
            obj.update_user = request.user
        else:
            obj.author = request.user   
        return super().save_model(request, obj, form, change)
    
    def get_prepopulated_fields(self, request, obj):
        return {"slug": ("title", )}


@admin.register(posts.FacultyAdministration)
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


@admin.register(posts.Departments)
class DepartmentsAdmin(admin.ModelAdmin):
    list_display_links = ("name", )
    list_display = ("id", "name", "faculty")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "faculty":
            try:
                kwargs["queryset"] = Posts.objects.filter(faculty=True)
            except Exception as e:
                kwargs["queryset"] = Posts.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_prepopulated_fields(self, request, obj):
        return {"slug": ("name", )}


@admin.register(posts.StudyProgram)
class StudyAdmin(admin.ModelAdmin):
    list_display_links = ("title", )
    list_display = ("id", "title", "year", "faculty")


@admin.register(posts.ContactSection)
class ContactSectionAdmin(admin.ModelAdmin):
    readonly_fields = ["get_image"]
    list_display_links = ("id", "title")
    list_display = ("id", "title", "order_num")

    fieldsets = (
        (None, {
            "fields": (
                "navbar", "title", ("image", "get_image"), "order_num", 
                "email", "phone", "address", "address_url"
            ),
        }),
    )
    

    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width='250' />")
    get_image.short_description = _("Tanlangan rasm")


@admin.register(posts.Workers)
class WorkersAdmin(admin.ModelAdmin):
    search_fields = ("f_name", )
    readonly_fields = ["get_image"]
    list_display_links = ("f_name", )
    list_display = ("id", "f_name", "section", "position", "phone", "email", "added_at")

    fieldsets = (
        (None, {
            "fields": (
                "position", "section", "f_name", "phone", "extra_phone", "email",
                ("image", "get_image")
            ),
        }),
    )

    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width='250' />")
    get_image.short_description = _("Tanlangan rasm")


@admin.register(posts.SectionsAndCenters)
class SectionsAdmin(admin.ModelAdmin):
    list_display_links = ("title", )
    list_display = ("id", "title", "added_at")
    prepopulated_fields = ({"slug": ("title", )})


    fieldsets = (
        (None, {
            "fields": (
                "navbar", "title", "about", 
                "target", "activity", "slug"
            ),
        }),
    )


@admin.register(posts.UniversityAdmistrations)
class UniversityAdminsAdmin(admin.ModelAdmin):
    list_editable = ("order_num", )
    readonly_fields = ("get_image", "added_at")
    prepopulated_fields = ({"slug": ("f_name", )})   
    list_display_links = ("id", "get_image", "f_name")
    list_display = ("id", "get_image", "f_name", "position", "order_num", "added_at")

    fieldsets = (
        ("Umumiy qiymatlar", {
            'fields': (
                "navbar", ("image", "get_image"), "facebook", 
                "instagram", "linkedin", "order_num", "email", "phone"
            ),
        }),
        ("O'zbek tilida", {
            'fields': (
                "f_name", "admission_days", "position", "short_info", 
                "scientific_activity", "scientific_direction", "main_tasks_in_position", 
            ),
        }),
        ("Automatik to'ldiriladigan fieldlar", {
            'fields': (
                "slug", "added_at"
            ),
        }),
    )

    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width='250' />")
    get_image.short_description = _("Tanlangan rasm")



@admin.register(posts.TalentedStudents)
class TalentedStudentsAdmin(admin.ModelAdmin):
    search_fields = ("f_name", )
    readonly_fields = ("get_image", )
    list_display_links = ("id", "get_image", "f_name")
    list_display = ("id", "get_image", "f_name", "desc", "added_at")

    fieldsets = (
        (None, {
            "fields": (
                "f_name", "desc", ("image", "get_image")
            ),
        }),
    )

    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width='250' />")
    get_image.short_description = _("Tanlangan rasm")


@admin.register(posts.BossSection)
class BossSection(admin.ModelAdmin):
    list_display = ("id", "f_name")
    list_display_links = ("id", "f_name")