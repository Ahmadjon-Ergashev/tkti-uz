import random
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


from main.models import posts, widgets


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


@admin.action(description=_("Nusxa ko'chirish"))
def simple_clone(modeladmin, request, queryset):
    for i in queryset:
        i.pk = None
        i.save()


@admin.register(posts.Navbar)
class NavbarAdmin(MPTTModelAdmin):
    """ Admin view for Navigation bar model """
    list_per_page = 10
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
            "classes": ("extrapretty", ),
            "fields": (
                "parent",
                "status", 
                "order_num", 
                "inside_order_num", 
                "visible", "url"
            ),
        }),
        (_("Nomi"), {
            "classes": ("extrapretty", ),
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


class ExtraFilesTabularInline(admin.TabularInline):
    model = widgets.ExtraFile
    extra = 1

    fieldsets = (
        (_("O'zbek tilida"), {
            'classes': ('collapse',),
            "fields": (
                "name_uz", "pdf_file"
            ),
        }),
        (_("Rus tilida"), {
            'classes': ('collapse',),
            "fields": (
                "name_ru", "pdf_file_en"
            ),
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse',),
            "fields": (
                "name_en", "pdf_file_ru"
            ),
        })
    )


@admin.register(posts.Posts)
class PostsAdmin(admin.ModelAdmin):
    """ Admin view for Posts """
    actions = (duplicate, )
    inlines = [ExtraFilesTabularInline]
    list_per_page = 10
    ordering = ("-added_at", )
    date_hierarchy = "added_at"
    list_editable = ("status", )
    list_display_links = ("title", )
    empty_value_display = "Tanlanmagan"
    search_fields = ("title", "navbar__name")
    list_filter = ("faculty", "navbar", "status", "author", "added_at")
    readonly_fields = ("author", "update_user", "updated_at", "get_image_file")
    list_display = ("id", "title", "navbar", "status", "post_viewed_count", "added_at")

    fieldsets = (
        (_("Umumiy o'zgaruvchilar"), {
            "classes": ("extrapretty", ),
            "fields": (
                "navbar", "status",
                "added_at", "author_post"                 
            ),
        }), 
        (_("Media fayllar"), {
            "fields": (
                ("image", "get_image_file"),
                ("pdf_file", "video_file", "zip_file")
            ),
        }),
        (_("O'zbek tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_uz", "subtitle_uz", "post_uz", "author_post_uz"
            ),
        }),
        (_("Rus tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_ru", "subtitle_ru", "post_ru", "pdf_file_ru", "author_post_ru"
            ),
        }),
        (_("Ingiliz tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_en", "subtitle_en", "post_en", "pdf_file_en", "author_post_en"
            ),
        }),
        (_("Automatik to'ldiriladigan fieldlar"), {
            "classes": ("collapse", ),
            "fields": (
                "author",
                "slug",
                "faculty",
                "post_viewed_count",
                "update_user",
                "updated_at"
            ),
        }),
    )

    def get_image_file(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' alt='asosiy rasm' width=100/>")
    get_image_file.short_description = _("Post uchun tanlangan rasmli fayl")

    def save_model(self, request, obj, form, change):
        if obj.navbar:
            if obj.navbar.slug == "fakultet":
                obj.faculty = True
        if obj.author:
            obj.update_user = request.user
        else:
            obj.author = request.user   
        return super().save_model(request, obj, form, change)
    
    def get_prepopulated_fields(self, request, obj):
        return {"slug": ("title_uz", )}

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related(
            "author", "update_user", "navbar")
        return qs


@admin.register(posts.FacultyAdministration)
class FacultyAdministrationAdmin(admin.ModelAdmin):
    actions = [clone]
    list_per_page = 10
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
                kwargs["queryset"] = posts.Posts.objects.filter(faculty=True)
            except Exception as e:
                kwargs["queryset"] = posts.Posts.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(posts.Departments)
class DepartmentsAdmin(admin.ModelAdmin):
    actions = [duplicate]
    list_per_page = 10
    search_fields = ("name_uz", )
    list_editable = ("faculty", )
    list_display_links = ("name_uz", )
    list_display = ("id", "name_uz", "faculty")
    readonly_fields = ("added_at", "post_viewed_count")

    fieldsets = (
        (None, {
            "fields": (
                "faculty",
                ("pdf_file", "pdf_file_en", "pdf_file_ru", "zip_file")
            ),
        }),
        (_("O'zbek tilida ma'lumotlar"), {
            'classes': ('collapse', ),
            "fields": (
                "name_uz", "about_uz", "target_uz", "activity_uz" 
            ),
        }),        
        (_("Rus tilida ma'lumotlar"), {
            'classes': ('collapse', ),
            "fields": (
                "name_ru", "about_ru", "target_ru", "activity_ru" 
            ),
        }),        
        (_("Ingiliz tilida ma'lumotlar"), {
            'classes': ('collapse', ),
            "fields": (
                "name_en", "about_en", "target_en", "activity_en" 
            ),
        }), 
        (_("Automatik to'ldiriladigan bo'limlar"), {
            'classes': ('collapse', ),
            "fields": (
                "slug", "added_at", "post_viewed_count"
            )
        })
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "faculty":
            try:
                kwargs["queryset"] = posts.Posts.objects.filter(faculty=True)
            except Exception as e:
                kwargs["queryset"] = posts.Posts.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_prepopulated_fields(self, request, obj):
        return {"slug": ("name_uz", )}


@admin.register(posts.DepartmentsAdmistrations)
class DeptAdminstraAdmin(admin.ModelAdmin):
    actions = [clone]
    list_per_page = 10
    search_fields = ("f_name_uz", )
    list_editable = ("order_num", ) 
    list_display_links = ("f_name_uz", )
    autocomplete_fields = ("department", )
    readonly_fields = ("get_image", "added_at", "updated_at", )
    list_display = ("id", "f_name_uz", "department", "order_num", "added_at")

    fieldsets = (
        (None, {
            "fields": (
                "department", ("image", "get_image"),
                "phone_number", "email"   
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


@admin.register(posts.ContactSection)
class ContactSectionAdmin(admin.ModelAdmin):
    actions = [simple_clone]
    list_per_page = 10
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


@admin.register(posts.SocialNetworksBoss)
class SocialNetworksBossAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    list_display_links = ("id", )
    list_editable = ("name", "icon", "color")
    list_display = ("id", "name", "icon", "color")


class NetworksBossAdmin(admin.TabularInline):
    model = posts.NetworksBoss
    extra = 1


@admin.register(posts.UniversityAdmistrations)
class UniversityAdminsAdmin(admin.ModelAdmin):
    actions = [duplicate]
    list_per_page = 10
    inlines = [NetworksBossAdmin]
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
        (_("Automatik to'ldiriladigan fieldlar"), {
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
    actions = [clone]
    list_per_page = 10
    search_fields = ("f_name_uz", )
    readonly_fields = ("get_image", "added_at")
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
        (_("Automatik to'ldiriladigan fieldlar"), {
            'fields': (
                "added_at",
            ),
        })
    )

    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width='250' />")
    get_image.short_description = _("Tanlangan rasm")


@admin.register(posts.SectionsBoss)
class BossSection(admin.ModelAdmin):
    actions = [clone]
    list_per_page = 10
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


@admin.register(posts.StudyDegrees)
class StudyDegreesAdmin(admin.ModelAdmin):
    actions = [simple_clone]
    list_per_page = 10
    search_fields = ("name_uz", )
    list_editable = ("order_num", )
    readonly_fields = ("added_at", )
    list_display_links = ("id", "name_uz")
    list_display = ("id", "name_uz", "order_num", "added_at")

    fieldsets = (
        (None, {
            "fields": (
                "order_num",
            )
        }),
        (_("O'zbek tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_uz",
            ),
        }),
        (_("Rus tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_ru",
            ),
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_en",
            ),
        }),
        (_("Automatik to'ldiriladigan fieldlar"), {
            'fields': (
                "added_at",
            ),
        })
    )


@admin.register(posts.FieldOfEducation)
class FieldOfEducationAdmin(admin.ModelAdmin):
    actions = [simple_clone]
    list_per_page = 10
    search_fields = ["name", ]
    readonly_fields = ("added_at", )
    list_display_links = ("id", "name")
    list_display = ("id", "name", "code", "added_at")
    
    fieldsets = (
        (None, {
            "fields": (
               "study_degree", "code" 
            ),
        }),
        (_("O'zbek tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_uz", 
            ),
        }),
        (_("Rus tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_ru", 
            ),
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_en", 
            ),
        }),
        (_("Automatik to'ldiriladigan fieldlar"), {
            'fields': (
                "added_at",
            ),
        })
    )


@admin.register(posts.LearningWay)
class LearningWayAdmin(admin.ModelAdmin):
    actions = [simple_clone]
    list_per_page = 10
    readonly_fields = ("added_at", )
    list_display_links = ("id", "name")
    list_display = ("id", "name", "study_degree", "fields_edu", "added_at")
    
    fieldsets = (
        (None, {
            "fields": (
               "study_degree", "fields_edu", "faculty", "image"
            ),
        }),
        (_("O'zbek tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_uz", "post_uz"
            ),
        }),
        (_("Rus tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_ru", "post_ru"
            ),
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_en", "post_en"
            ),
        }),
        (_("Automatik to'ldiriladigan fieldlar"), {
            'fields': (
                "added_at",
            ),
        })
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "faculty":
            try:
                kwargs["queryset"] = posts.Posts.objects.filter(faculty=True)
            except Exception as e:
                kwargs["queryset"] = posts.Posts.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(posts.ModuleOfStudyPrograme)
class ModuleOfStudyProgramAdmin(admin.ModelAdmin):
    model = posts.ModuleOfStudyPrograme
    list_per_page = 10
    actions = [simple_clone]
    search_fields = ("name_uz", )
    readonly_fields = ("added_at", )
    list_display_links = ("id", "name_uz")
    list_display = ("id", "name_uz", "semester", "educational_area", "added_at")

    fieldsets = (
        (None, {
            "fields": (
               "semester", "educational_area",
            ),
        }),
        (_("O'zbek tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_uz", "pdf_file",
            ),
        }),
        (_("Rus tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_ru", "pdf_file_ru",
            ),
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_en", "pdf_file_en",
            ),
        }),
        (_("Automatik to'ldiriladigan fieldlar"), {
            'fields': (
                "added_at",
            ),
        })
    )


class ModuleOfStudyProgrameTabularInline(admin.TabularInline):
    model = posts.ModuleOfStudyPrograme
    extra = 1
    exclude = ["name"]


class AboutStudyProgramPDFTabularInline(admin.TabularInline):
    model = posts.AboutStudyProgramPDF
    extra = 1


class EntryRequirementsTabularInline(admin.TabularInline):
    model = posts.EntryRequirements
    extra = 1
    exclude = ["requirement"]


# class ThemeEducationTabularInline(admin.TabularInline):
#     model = posts.ThemesForEducation
#     extra = 1
#     exclude = ["name", "desc"]

@admin.register(posts.ThemesForEducation)
class ThemesForEducationAdmin(admin.ModelAdmin):
    actions = [simple_clone]
    search_fields = ("name", )
    list_display = ("id", "name")
    exclude = ("name", "desc", "teacher", "finance")


@admin.register(posts.EducationalAreas)
class EducationalAreasAdmin(admin.ModelAdmin):
    list_per_page = 10
    actions = [simple_clone]
    search_fields = ("name_uz", )
    list_display_links = ("id", "name_uz")
    list_display = ("id", "name_uz", "added_at")
    readonly_fields = ("added_at", "post_viewed_count")
    inlines = [
        ModuleOfStudyProgrameTabularInline,
        AboutStudyProgramPDFTabularInline,
        EntryRequirementsTabularInline
    ]

    fieldsets = (
        (None, {
            "fields": (
                "study_way", "author_post", "phone", "extra_phone", "email",
                "full_time_fee", "dept_fee",
                ("pdf_file", "pdf_file_en", "pdf_file_ru")
            ),
        }),
        (_("O'zbek tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_uz", "desc_uz", "application_procedure_uz",
                "tuition_fee_uz", "address_uz", ("you_may_become_image", "you_may_become_uz")
            ),
        }),
        (_("Rus tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_ru", "desc_ru", "application_procedure_ru",
                "tuition_fee_ru", "address_ru", "you_may_become_ru"
            ),
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_en", "desc_en", "application_procedure_en",
                "tuition_fee_en", "address_en", "you_may_become_en"
            ),
        }),
        (_("Automatik to'ldiriladigan fieldlar"), {
            'fields': (
                "added_at", "post_viewed_count"
            ),
        })
    )





