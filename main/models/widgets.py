from django.db import models
from colorfield.fields import ColorField
from django.utils.translation import gettext_lazy as _

class SocialNetworks(models.Model):
    """ for social networks models exa: facebook, telegram and ... """
    name = models.CharField(max_length=50, verbose_name=_("Nomi"), unique=True, null=True, help_text=_("ishtimoiy tarmoq nomlarini kiriting, m: facebook, instagram"))
    icon = models.CharField(max_length=50, verbose_name=_("Icon"), null=True, help_text=_("messangerning icon class nomi, class nomlarini olish uchun https://fontawesome.com/v5/search shu saytga kiring, m: fab fa-facebook"))
    color = ColorField(verbose_name=_("rangi"), null=True)
    url = models.URLField(verbose_name=_("url manzil"))