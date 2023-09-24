from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _



class SocialNetworks(models.Model):
    """ for social networks models exa: facebook, telegram and ... """
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="author_networking")
    name = models.CharField(max_length=50, verbose_name=_("Nomi"), unique=True, null=True, help_text=_("ishtimoiy tarmoq nomlarini kiriting, m: facebook, instagram"))
    icon = models.CharField(max_length=50, verbose_name=_("Icon"), null=True, help_text=_("messangerning icon class nomi, class nomlarini olish uchun https://fontawesome.com/v5/search shu saytga kiring, m: fab fa-facebook"))
    color = ColorField(verbose_name=_("rangi"), null=True)
    url = models.URLField(verbose_name=_("url manzil"))
    order_num = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="update_network_user")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'social_networks'
        managed = True
        verbose_name = _("Ijtimoiy tarmoqlar")
        verbose_name_plural = _("Ijtimoiy tarmoqlar")

    def __str__(self):
        return str(self.name) if self.name else None


class HeaderIMG(models.Model):
    """ header image model """
    image = models.ImageField(verbose_name=_("Bosh sahifa uchun rasm"), upload_to="HeaderIMG/%Y-%m-%d/")
    order_num = models.IntegerField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "header_img"
        managed = True
        verbose_name = _("Bosh sahifa uchun rasmlar")
        verbose_name_plural = _("Bosh sahifa uchun rasmlar")

    def __str__(self):
        return f"Image {self.id}"
    