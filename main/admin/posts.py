import random
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from guardian.admin import GuardedModelAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


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
    ordering = ("name_uz", )
    date_hierarchy = "added_at"
    list_display_links = ("name_uz", )
    search_fields = ("name_uz", "name_ru", "name_en")
    list_editable = ("order_num", "status", "inside_order_num")
    list_filter = ("parent", "added_at", "status", "visible", "author")
    readonly_fields = ("author", "added_at", "update_user", "updated_at")
    list_display = ("id", "name_uz", "parent", "status", "order_num", "inside_order_num", "visible", "added_at")

    fieldsets = (
        (_("Umumiy o'zgaruvchilar"), {
            "classes": ("extrapretty"),
            "fields": (
                "parent",
                "status", 
                "order_num", 
                "inside_order_num", 
                "visible"        
            ),
        }),
        (_("Nomi"), {
            "classes": ("extrapretty"),
            "fields": (
                "name_uz",             
                "name_ru",             
                "name_en"             
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
        return {"slug": ("name_uz", )}



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
            "classes": ("collapse", ),
            "fields": (
                "title_uz", "subtitle_uz", "post_uz"                
            ),
        }),
        (_("Rus tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_ru", "subtitle_ru", "post_ru"                
            ),
        }),
        (_("Ingiliz tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_en", "subtitle_en", "post_en"                
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
        return {"slug": ("title_uz", )}


@admin.register(posts.FacultyAdministration)
class FacultyAdmistrationAdmin(GuardedModelAdmin):
    actions = [clone]
    ordering = ("order_num", )
    list_filter = ("added_at", )
    list_editable = ("order_num", )
    list_display_links = ("f_name_uz", )
    readonly_fields = ("get_image", "added_at", "updated_at")
    list_display = ("id", "f_name_uz", "order_num", "job_name_uz", "phone_number", "added_at")
    search_fields = ("f_name_uz", "f_name_en", "f_name_ru", "job_name_uz", "job_name_ru", "job_name_en")

    fieldsets = (
        (_("Umumiy o'zgaruvchilar"), {
            "fields": (
              "faculty", "phone_number", "email", "order_num", ("image", "get_image")
            ),
        }),
        (_("O'zbek tilida ma'lumotlar"), {
            'classes': ('collapse', ),
            "fields": (
                "f_name_uz", "job_name_uz", "admission_day_uz"
            ),
        }),        
        (_("Rus tilida ma'lumotlar"), {
            'classes': ('collapse', ),
            "fields": (
                "f_name_ru", "job_name_ru", "admission_day_ru"
            ),
        }),        
        (_("Ingiliz tilida ma'lumotlar"), {
            'classes': ('collapse', ),
            "fields": (
                "f_name_en", "job_name_en", "admission_day_en"
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
                kwargs["queryset"] = posts.Posts.objects.filter(navbar__slug="fakultet")
            except Exception as e:
                kwargs["queryset"] = posts.Posts.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(posts.Departments)
class DepartmentsAdmin(admin.ModelAdmin):
    list_display_links = ("name_uz", )
    list_display = ("id", "name_uz", "faculty")

    # fieldsets = (
    #     (None, {
    #         "fields": (
                
    #         ),
    #     }),
    # )
    

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "faculty":
            try:
                kwargs["queryset"] = posts.Posts.objects.filter(faculty=True)
            except Exception as e:
                kwargs["queryset"] = posts.Posts.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_prepopulated_fields(self, request, obj):
        return {"slug": ("name_uz", )}


@admin.register(posts.StudyProgram)
class StudyAdmin(admin.ModelAdmin):
    list_display_links = ("title_uz", )
    list_display = ("id", "title_uz", "year", "faculty")

    fieldsets = (
        (None, {
            "fields": (
                "year", "faculty", "department", "study_way", "pdf_file", "study_time"
            ),
        }),
        (_("O'zbek tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "title_uz", 
            ),
        }),
        (_("Rus tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "title_ru", 
            ),
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "title_en", 
            ),
        }),
    )
    


@admin.register(posts.ContactSection)
class ContactSectionAdmin(admin.ModelAdmin):
    readonly_fields = ["get_image"]
    list_display_links = ("id", "title")
    list_display = ("id", "title", "order_num")

    fieldsets = (
        (None, {
            "fields": (
                "navbar", ("image", "get_image"), "order_num", 
                "email", "phone", "address_url"
            ),
        }),
        (_("O'zbek tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "title_uz", "address_uz"
            ),
        }),
        (_("Rus tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "title_ru", "address_ru"
            ),
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "title_en", "address_en"
            ),
        }),
    )
    

    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width='250' />")
    get_image.short_description = _("Tanlangan rasm")


@admin.register(posts.Workers)
class WorkersAdmin(admin.ModelAdmin):
    readonly_fields = ["get_image"]
    list_display_links = ("f_name_uz", )
    search_fields = ("f_name_uz", "f_name_ru", "f_name_en")
    list_display = ("id", "f_name_uz", "section", "position", "phone", "email", "added_at")

    fieldsets = (
        (None, {
            "fields": (
                "position", "section", "phone", "extra_phone", "email",
                ("image", "get_image")
            ),
        }),
        (_("O'zbek tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "f_name_uz", 
            ),
        }),
        (_("Rus tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "f_name_ru", 
            ),
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "f_name_en", 
            ),
        }),
    )

    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width='250' />")
    get_image.short_description = _("Tanlangan rasm")


@admin.register(posts.SectionsAndCenters)
class SectionsAdmin(admin.ModelAdmin):
    list_display_links = ("title_uz", )
    list_display = ("id", "title_uz", "added_at")
    prepopulated_fields = ({"slug": ("title_uz", )})


    fieldsets = (
        (None, {
            "fields": (
                "navbar", 
            ),
        }),
        (_("O'zbek tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "title_uz", "about_uz", "target_uz", "activity_uz" 
            ),
        }),
        (_("Rus tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "title_ru", "about_ru", "target_ru", "activity_ru" 
            ),
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "title_en", "about_en", "target_en", "activity_en" 
            ),
        }),
        (_("Automatik to'ldiriladigan fieldlar"), {
            'classes': ('collapse', ),
            "fields": (
                "slug",
            ),
        }),
    )


@admin.register(posts.UniversityAdmistrations)
class UniversityAdminsAdmin(admin.ModelAdmin):
    list_editable = ("order_num", )
    readonly_fields = ("get_image", "added_at")
    prepopulated_fields = ({"slug": ("f_name_uz", )})   
    list_display_links = ("id", "get_image", "f_name_uz")
    list_display = ("id", "get_image", "f_name_uz", "position", "order_num", "added_at")

    fieldsets = (
        ("Umumiy qiymatlar", {
            'fields': (
                "navbar", ("image", "get_image"), "facebook", 
                "instagram", "linkedin", "order_num", "email", "phone"
            ),
        }),
        ("O'zbek tilida", {
            'fields': (
                "f_name_uz", "admission_days_uz", "position_uz", "short_info_uz", 
                "scientific_activity_uz", "scientific_direction_uz", "main_tasks_in_position_uz", 
            ),
        }),
        ("Rus tilida", {
            'fields': (
                "f_name_ru", "admission_days_ru", "position_ru", "short_info_ru", 
                "scientific_activity_ru", "scientific_direction_ru", "main_tasks_in_position_ru", 
            ),
        }),
        ("Ingiliz tilida", {
            'fields': (
                "f_name_en", "admission_days_en", "position_en", "short_info_en", 
                "scientific_activity_en", "scientific_direction_en", "main_tasks_in_position_en", 
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
    search_fields = ("f_name_uz", )
    readonly_fields = ("get_image", )
    list_display_links = ("id", "get_image", "f_name_uz")
    list_display = ("id", "get_image", "f_name_uz", "desc_uz", "added_at")

    fieldsets = (
        (None, {
            "fields": (
                ("image", "get_image")
            ),
        }),
        (_("O'zbek tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "f_name_uz", "desc_uz",
            ),
        }),
        (_("Rus tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "f_name_ru", "desc_ru",
            ),
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "f_name_en", "desc_en",
            ),
        }),
    )

    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width='250' />")
    get_image.short_description = _("Tanlangan rasm")


@admin.register(posts.BossSection)
class BossSection(admin.ModelAdmin):
    list_display = ("id", "f_name")
    readonly_fields = ("get_image", )
    list_display_links = ("id", "f_name")

    fieldsets = (
        (None, {
            "fields": (
                "post",
                "position", "email", "phone",
                ("f_name_uz", "f_name_ru", "f_name_en"),
                ("image", "get_image")
            ),
        }),
    )

    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width='250' />")
    get_image.short_description = _("Tanlangan rasm")
    