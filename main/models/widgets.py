import os
from io import BytesIO
from django.db import models
from PIL import Image, ImageOps
from django.core.files import File
from colorfield.fields import ColorField
from django_quill.fields import QuillField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class NavbarStatus(models.TextChoices):
    base = "base", _("Asosiy")
    inside = "inside", _("Ichki")


class StudyWayType(models.TextChoices):
    high: str = "high", _("Bakalavriat")
    higher: str = "higher", _("Magistraturat")


class StudyTimes(models.TextChoices):
    daytime: str = "daytime", _("Kundizgi")
    evning: str = "evning", _("Kechgi")
    outer: str = "outer", _("Sirtqi")


class Status(models.TextChoices):
    published: str = "pub", _("Published")
    pendding: str = "pen", _("Pendding")


class WorkerPositions(models.TextChoices):
    department_head: str = _("Bo'lim boshlig'i"), _("Bo'lim boshlig'i")
    chief_specialist: str = _("Bosh mutaxasis"), _("Bosh mutaxasis")
    leading_specialist: str = _("Yetakchi mutaxasis"), _("Yetakchi mutaxasis")


class AbstractTemplate(models.Model):
    """ abstract tamplate for news posts and ads """
    image = models.ImageField(verbose_name=_("Asosiy rasm"), upload_to="image/%Y-%m-%d/", default="default/default.png", null=True)
    title = models.CharField(verbose_name=_("Sarlavha"), max_length=230, null=True)
    subtitle = models.CharField(verbose_name=_("Qisqacha mazmun"), max_length=255, null=True)
    post = QuillField(verbose_name=_("To'liq mazmuni"), null=True, blank=True)
    status = models.CharField(verbose_name=_("status"), max_length=50, choices=Status.choices, default=Status.pendding)
    slug = models.SlugField(max_length=255, verbose_name="slug", unique=True, help_text=_("Majburyat tug'ulmasa tegmang"))
    post_viewed_count = models.IntegerField(default=0, verbose_name=_("Ko'rilganlik soni"), help_text=_("Tegilmasin !"))
    author_post = models.CharField(verbose_name=_("Muallifi"), max_length=300, default="TKTI axborot xizmati")
    added_at = models.DateTimeField(verbose_name=_("Vaqt & sana"))
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        managed = True

    
class Hashtag(models.Model):
    """ hashtags for news and ads """
    name = models.CharField(max_length=123, verbose_name=_("Nomi"), null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "hashtags"
        managed = True
        verbose_name = _("Hashtaglar")
        verbose_name_plural = _("Hashtaglar")


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
        return f"Image {self.pk}"
    
    def save(self, *args, **kwargs):
        if self._state.adding:
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
        else:
            super().save(*args, **kwargs)
    

class UsefullLinks(models.Model):
    """ foydali havolar uchun model """
    name = models.CharField(verbose_name=_("Nomi"), max_length=255, unique=True)
    logo = models.ImageField(verbose_name=_("rasmi"), default="default/gerb.png", null=True, blank=True, upload_to="image/usefull_links/%Y-%m-%d/")
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
    

class Year(models.Model):
    """ model for years """
    year = models.CharField(max_length=4, verbose_name=_("Yilni kiriting"))

    class Meta:
        db_table = 'years'
        managed = True
        verbose_name = _("Yil")
        verbose_name_plural = _("Yillar")
    
    def __str__(self):
        return self.year


class PhotoGallary(models.Model):
    """ photos model """
    image = models.ImageField(_("Rasm"), upload_to="image/photo_gallary/%Y-%m-%d/", null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "photo_gallary"
        managed = True
        ordering = ["-added_at"]
        verbose_name = _("Rasmlar")
        verbose_name_plural = _("Rasmlar")

    def __str__(self):
        return f"{self.image}"
    
    def save(self, *args, **kwargs):
        if self._state.adding:
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
        else:
            super().save(*args, **kwargs)


class Flag(models.Model):
    """ flag model """
    title = models.CharField(_("Sarlavha"), max_length=255)
    description = QuillField(_("To'liq Matn"), null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'flag'
        managed = True
        verbose_name = _("Bayroq")
        verbose_name_plural = _("Bayroq")


class CoatofArms(models.Model):
    """ coat of arms (gerb) model """
    title = models.CharField(_("Sarlavha"), max_length=255)
    description = QuillField(_("To'liq Matn"), null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'coat_of_arms'
        managed = True
        verbose_name = _("Gerb")
        verbose_name_plural = _("Gerb")


class Anthem(models.Model):
    """ anthem model """
    title = models.CharField(_("Sarlavha"), max_length=255)
    description = QuillField(_("To'liq Matn"), null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'anthem'
        managed = True
        verbose_name = _("Madhiya")
        verbose_name_plural = _("Madhiya")