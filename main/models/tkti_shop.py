from django.db import models
from django.utils.translation import gettext_lazy as _


class ShopCategory(models.Model):
	name = models.CharField(max_length=255, null=False, blank=False, verbose_name=_("Nomi"))

	def __str__(self):
		return self.name

	class Meta:
		ordering = ("name", )
		db_table = 'shop_category'
		verbose_name = _("Shop Bo'limlari")
		verbose_name_plural = _("Shop Bo'limlari")


class Shop(models.Model):
	category = models.ForeignKey(ShopCategory, on_delete=models.SET_NULL, null=True, blank=True)
	name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Nomi"))
	image = models.ImageField(upload_to="tkti_shop_images/", null=True, blank=True)
	price = models.DecimalField(decimal_places=2, max_digits=15, null=True, blank=True)
	contact = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Ma'sul shaxs"))
	phone_number = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Telefon raqam"))
	telegram = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Telegram manzil"))
	instagram = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Instagram link"))
	added_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'shop'
		ordering = ("-added_at", )
		verbose_name = _("TKTI Shop")
		verbose_name_plural = _("TKTI Shop")
