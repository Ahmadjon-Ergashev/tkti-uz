from django.contrib import admin
from django.utils.translation import gettext_lazy as _

import main.models as models


@admin.action(description=_("Nusxa ko'chirish"))
def simple_clone(modeladmin, request, queryset):
	for i in queryset:
		i.pk = None
		i.save()


@admin.register(models.ShopCategory)
class ShopCategoryAdmin(admin.ModelAdmin):
	actions = [simple_clone]
	list_display = ("id", "name")
	list_display_links = ("name",)
	exclude = ("name",)


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
	actions = [simple_clone]
	list_display_links = ("id", "name")
	list_display = ("id", "name", "category")
	exclude = ("name",)
