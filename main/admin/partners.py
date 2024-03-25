from django.contrib import admin

import main.models as models


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
	exclude = ("name", )
	list_display = ('id', 'name')
	list_display_links = ("id", "name")


@admin.register(models.Partner)
class PartnerAdmin(admin.ModelAdmin):
	exclude = ("name", )
	search_fields = ("name", )
	list_filter = ("country", )
	list_display_links = ("name", )
	list_display = ("id", "name", "country")
