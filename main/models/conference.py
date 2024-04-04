from django.db import models
import main.models as model
from django.utils.translation import gettext_lazy as _


class Conference(model.AbstractTemplate):

	def __str__(self):
		return self.title

	class Meta:
		db_table = 'conferences'
		ordering = ("-added_at", )
		verbose_name = _("Konfirensalar")
		verbose_name_plural = _("Konfirensalar")

