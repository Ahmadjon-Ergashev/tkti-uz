from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
	name = models.CharField(max_length=255, verbose_name=_("Nomi"), null=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'country'
		ordering = ("name", )
		verbose_name = _("Davlatlar")
		verbose_name_plural = _("Davlatlar")


class Partner(models.Model):
	name = models.CharField(max_length=255, verbose_name=_("Nomi"), null=True, blank=True)
	image = models.ImageField(upload_to="partners/", null=True, blank=True)
	url = models.URLField(null=True, blank=True, max_length=400, verbose_name=_("URL manzil"))
	country = models.ForeignKey(
		Country, on_delete=models.SET_NULL, related_name="partners_country",
		verbose_name=_("Davlat"), null=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'partners'
		ordering = ("country", )
		verbose_name = _("Hamkorlar")
		verbose_name_plural = _("Hamkorlar")

