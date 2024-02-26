from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from main.models import widgets


@admin.action(description=_("Nusxa ko'chirish"))
def simple_clone(modeladmin, request, queryset):
    for i in queryset:
        i.pk = None
        i.save()


@admin.register(widgets.SocialNetworks)
class SocialNetworkingAdmin(admin.ModelAdmin):     
    list_per_page = 10
    actions = [simple_clone]
    ordering = ("-added_at", )
    search_fields = ("name_uz", )
    list_display_links = ("name_uz", )
    list_editable = ("order_num", "color")
    list_display = ("id", "name_uz", "order_num", "color", "added_at")
    readonly_fields = ("author", "update_user", "added_at", "updated_at" )

    fieldsets = (
        (None, {
            'fields': (
                "order_num", "color", "icon", "url"
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
            'classes': ('collapse', ),
            'fields': (
                "author", "update_user", "added_at", "updated_at"
            ),
        })
    )

    def save_model(self, request, obj, form, change):
        if obj.author:
            obj.update_user = request.user
        else:
            obj.author = request.user
        return super().save_model(request, obj, form, change)
    

@admin.register(widgets.HeaderIMG)
class HeaderIMGAdmin(admin.ModelAdmin):
    list_per_page = 10
    actions = [simple_clone]
    list_editable = ("order_num", )
    readonly_fields = ["get_image"]
    list_display_links = ("get_image", )
    list_display = ("id", "get_image", "order_num", "add_time")

    def get_image(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width=100 />")


@admin.register(widgets.UsefullLinks)
class LinksAdmin(admin.ModelAdmin):
    list_per_page = 10
    actions = [simple_clone]
    list_display_links = ("name_uz", )
    readonly_fields = ("add_time", "get_logo",)
    search_fields = ("name_uz", "name_ru", "name_en")
    list_display = ("id", "name_uz", "get_logo", "add_time")

    fieldsets = (
        (None, {
            "fields": (
                ("logo", "get_logo"), "link"
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
                "add_time", 
            ),
        }),
    )
    
    def get_logo(self, obj):
        return mark_safe(f"<img src='{obj.logo.url}' width=100 />")
    

@admin.register(widgets.QuickLinks)
class QuickLinksAdmin(admin.ModelAdmin):
    list_per_page = 10
    ordering = ("-added_at", )
    actions = [simple_clone]
    readonly_fields = ("added_at", )
    list_display_links = ("name_uz", )
    list_editable = ("order_num", "url")
    list_display = ("id", "name_uz", "order_num", "url", "added_at")

    fieldsets = (
        (None, {
            "fields": (
                "order_num", "url"
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
        }),
    )
    

@admin.register(widgets.EventTypes)
class EventTypesAdmin(admin.ModelAdmin):
    list_per_page = 10
    ordering = ("-added_at", )
    actions = [simple_clone]
    readonly_fields = ("added_at", )
    list_display_links = ("name_uz", )
    list_display = ("id", "name_uz", "added_at")

    fieldsets = (
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
        }),
    )
    

@admin.register(widgets.Statistika)
class StatistikaAdmin(admin.ModelAdmin):
    list_per_page = 10
    ordering = ("-added_at", )
    actions = [simple_clone]
    readonly_fields = ("added_at", )
    list_display_links = ("name_uz", )
    list_editable = ("order_num", "quantity")
    list_display = ("id", "name_uz", "quantity", "order_num", "added_at")

    fieldsets = (
        (None, {
            "fields": (
                "order_num", "quantity", "icon", "url"
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
        }),
    )


admin.site.register(widgets.Year)
admin.site.register(widgets.Hashtag)


@admin.register(widgets.Flag)
class FlagAdmin(admin.ModelAdmin):
    list_per_page = 10
    actions = [simple_clone]
    list_display = ("id", "title_uz")
    list_display_links = ("title_uz", )

    fieldsets = (
        (_("O'zbek tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_uz", "description_uz"
            ),
        }),
        (_("Rus tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_ru", "description_ru"
            ),
        }),
        (_("Ingiliz tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_en", "description_en"
            ),
        }),
    )
    


@admin.register(widgets.CoatofArms)
class CoatofArmsAdmin(admin.ModelAdmin):
    actions = [simple_clone]
    list_per_page = 10
    list_display = ("id", "title_uz")
    list_display_links = ("title_uz", )

    fieldsets = (
        (_("O'zbek tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_uz", "description_uz"
            ),
        }),
        (_("Rus tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_ru", "description_ru"
            ),
        }),
        (_("Ingiliz tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_en", "description_en"
            ),
        }),
    )


@admin.register(widgets.Anthem)
class AnthemAdmin(admin.ModelAdmin):
    actions = [simple_clone]
    list_per_page = 10
    list_display = ("id", "title_uz")
    list_display_links = ("title_uz", )

    fieldsets = (
        (_("O'zbek tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_uz", "description_uz"
            ),
        }),
        (_("Rus tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_ru", "description_ru"
            ),
        }),
        (_("Ingiliz tilida"), {
            "classes": ("collapse", ),
            "fields": (
                "title_en", "description_en"
            ),
        }),
    )


@admin.register(widgets.FaqCategory)
class FaqCategoryAdmin(admin.ModelAdmin):
    actions = [simple_clone]
    list_per_page = 10
    list_display = ("id", "name")
    list_display_links = ("id", "name")

    fieldsets = (
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
    )


@admin.register(widgets.Faq)
class FaqAdmin(admin.ModelAdmin):
    actions = [simple_clone]
    list_per_page = 10
    list_filter = ("category", )
    list_editable = ("is_active", )
    readonly_fields = ("added_at", )
    list_display_links = ("id", "title_uz")
    list_display = ("id", "title_uz", "category", "is_active", "added_at")

    fieldsets = (
        (None, {
            "fields": (
                ("category", "is_active"), 
            ),
        }),
        (_("O'zbek tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "title_uz", "answer_uz"
            ),
        }),
        (_("Rus tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "title_ru", "answer_ru" 
            ),
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "title_en", "answer_en" 
            ),
        }),
        (_("Automatik to'ldiriladigan fieldlar"), {
            'fields': (
                "added_at", 
            ),
        }),
    )


@admin.register(widgets.Semesters)
class SemestersAdmin(admin.ModelAdmin):
    list_per_page = 10
    actions = [simple_clone]
    list_display = ("id", "name")
    readonly_fields = ("added_at", )
    list_display_links = ("id", "name")

    fieldsets = (
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
        }),
    )


@admin.register(widgets.Digitization)
class DigitizationAdmin(admin.ModelAdmin):
    list_per_page = 10
    actions = [simple_clone]
    list_display = ("id", "name")
    readonly_fields = ("added_at", )
    list_display_links = ("id", "name")

    fieldsets = (
        (None, {
            "fields": (
                "icon", "url"
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
        }),
    )


@admin.register(widgets.BRMItems)
class BRMItemsAdmin(admin.ModelAdmin):
    list_per_page = 10
    actions = [simple_clone]
    list_display = ("id", "name")
    readonly_fields = ("added_at", )
    list_display_links = ("id", "name")

    fieldsets = (
        (None, {
            "fields": (
                "image", "color", "number", "video_file"
            ),
        }),
        (_("O'zbek tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_uz", "desc_uz", "pdf_file"
            )
        }),
        (_("Rus tilida"), {
            'classes': ('collapse', ),
            "fields": (
                "name_ru", "desc_ru", "pdf_file_ru"
            )
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse',),
            "fields": (
                "name_en", "desc_en", "pdf_file_en"
            )
        }),
        (_("Automatik to'ldiriladigan fieldlar"), {
            'fields': (
                "added_at",
            ),
        }),
    )


@admin.register(widgets.FinancialBenefit)
class FinancialBenefitAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ("name", )
    list_filter = ("added_at", )
    readonly_fields = ("added_at", )
    list_display_links = ("id", "name")
    list_display = ("id", "name", "added_at")

    fieldsets = (
        (None, {"fields": ("icon", )}),
        (_("O'zbek tilida"), {
            'classes': ('collapse',),
            "fields": (
                "name_uz", "about_uz", "responsible_organization_uz",
                "for_who_uz", "deadline_uz", "main_lower_uz", "contact_uz"
            )
        }),
        (_("Rus tilida"), {
            'classes': ('collapse',),
            "fields": (
                "name_ru", "about_ru", "responsible_organization_ru",
                "for_who_ru", "deadline_ru", "main_lower_ru", "contact_ru"
            )
        }),
        (_("Ingiliz tilida"), {
            'classes': ('collapse',),
            "fields": (
                "name_en", "about_en", "responsible_organization_en",
                "for_who_en", "deadline_en", "main_lower_en", "contact_en"
            )
        }),
        (_("Automatik to'ldiriladigan fieldlar"), {
            'classes': ('collapse',),
            'fields': (
                "added_at",
            ),
        }),
    )
