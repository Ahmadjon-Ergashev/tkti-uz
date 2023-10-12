from django.db import models
from django_quill.fields import QuillField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

import os
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files import File

#local
from .posts import Status


class ObjectType(models.TextChoices):
    news: str = "news", _("Yangilik")
    ads: str = "ads", _("E'lon")


class NewsAndAds(models.Model):
    """ model for news and announcement  """
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="author_news")
    image = models.ImageField(verbose_name=_("Asosiy rasm"), upload_to="image/news/%Y-%m-%d/", default="default/default.png", null=True)
    object_type = models.CharField(max_length=100, verbose_name=_("Ma'lumot turi"), choices=ObjectType.choices, default=ObjectType.news)
    title = models.CharField(verbose_name=_("Sarlavha"), max_length=255, null=True)
    subtitle = models.CharField(verbose_name=_("Qisqacha mazmuni"), max_length=300, null=True)
    post = QuillField(verbose_name=_("To'liq mazmuni"), null=True)
    pdf_file = models.FileField(
        verbose_name=_("PDF fayl"), upload_to="pdf/news/%Y-%m-%d/", 
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    video_file = models.FileField(
        verbose_name=_("Video fayl"), upload_to="videos/news/%Y-%m-%d/",
        null=True, blank=True, help_text=_("agar video fayl mavjud bo'lsa yuklang.")
    )
    status = models.CharField(verbose_name=_("status"), max_length=50, choices=Status.choices, default=Status.pendding)
    slug = models.SlugField(max_length=255, verbose_name="slug", unique=True, help_text=_("Majburyat tug'ulmasa tegmang"))
    post_viewed_count = models.IntegerField(default=0, verbose_name=_("Ko'rilganlik soni"), help_text=_("Tegilmasin !"))
    author_post = models.CharField(verbose_name=_("Yangilik yoki E'lon muallifi"), max_length=300, default="TKTI axborot xizmati")
    added_at = models.DateTimeField(verbose_name=_("Vaqt & sana"))
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="update_news_user")
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "news"
        managed = True
        verbose_name = _("Yangiliklar va E'lonlar")
        verbose_name_plural = _("Yangiliklar va E'lonlar")


    def __str__(self):
        return str(self.title) if self.title else None

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
    
    




