from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

import os
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files import File



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
    image = models.ImageField(verbose_name=_("Bosh sahifa uchun rasm"), upload_to="image/HeaderIMG/%Y-%m-%d/")
    order_num = models.IntegerField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "header_img"
        managed = True
        verbose_name = _("Bosh sahifa uchun rasmlar")
        verbose_name_plural = _("Bosh sahifa uchun rasmlar")

    def __str__(self):
        return f"Image {self.id}"
    
    def save(self, *args, **kwargs):
        im = Image.open(self.image)
        im = im.convert('RGB')
        im = ImageOps.exif_transpose(im)
        im_io = BytesIO()
        im.save(im_io, 'JPEG', quality=50)
        filename = os.path.splitext(self.image.name)[0]
        filename = f"{filename}.jpg"
        new_image = File(im_io, name=filename)
        self.image = new_image
        super().save(*args, **kwargs)
    

class UsefullLinks(models.Model):
    """ foydali havolar uchun model """
    name = models.CharField(verbose_name=_("Nomi"), max_length=255, unique=True)
    logo = models.ImageField(verbose_name=_("rasmi"), default="default/gerb.png", upload_to="image/usefull_links/%Y-%m-%d/")
    link = models.URLField(verbose_name=_("Saytga havola"), max_length=150)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "usefull_links"
        managed = True
        verbose_name = "Foydali havolalar"
        verbose_name_plural = "Foydali havolalar"
    
    def __str__(self):
        return str(self.name) if self.name else None
    

class QuickLinks(models.Model):
    """ tezkor havolalar """
    name = models.CharField(max_length=100, verbose_name=_("Nomi"), unique=True, null=True)
    url = models.URLField(_("url manzili"), max_length=300, null=True, blank=True)
    order_num = models.IntegerField(default=0, verbose_name=_("Tartib raqami"))
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "quick_links"
        managed = True
        verbose_name = "Tezkor havolalar"
        verbose_name_plural = "Tezkor havolalar"

    def __str__(self):
        return str(self.name) if self.name else None
    

class Statistika(models.Model):
    """ universitet xaqida statistik malumotlar """
    name = models.CharField(_("Nomi"), max_length=80, unique=True)
    icon = models.CharField(_("icon"), max_length=50, null=True)
    quantity = models.IntegerField(_("soni"), default=0)
    order_num = models.IntegerField(_("Tartib raqam"), default=0)
    added_at = models.DateTimeField(auto_now_add=True)   

    class Meta:
        db_table = "statistika"
        managed = True
        verbose_name = _("Statistika")
        verbose_name_plural = _("Statistika")
    
    def __str__(self):
        return self.name if self.name else None