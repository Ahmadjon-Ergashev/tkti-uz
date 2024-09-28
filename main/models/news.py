from django.db import models
from django_quill.fields import QuillField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

import os
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files import File

# local
from main.models import widgets
from main.models import posts
from main.models import sections_and_centers


class Category(models.Model):
    """ category model for news and ads  """
    name = models.CharField(verbose_name=_("Nomi"), max_length=123, null=True)
    slug = models.SlugField(max_length=123, unique=True, verbose_name=_('slug'),
                            help_text=_("Majburyat tug'ulmasa tegmang !"))
    order_num = models.IntegerField(default=0, verbose_name=_("Tartib raqami"))
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'category_news'
        managed = True
        verbose_name = _("Yangiliklar uchun bo'limlar")
        verbose_name_plural = _("Yangiliklar uchun bo'limlar")

    def __str__(self):
        return f"{self.name}"


class News(widgets.AbstractTemplate):
    """ model for news """
    faculty_dact = models.ManyToManyField(posts.Posts,
                                          verbose_name=_("Yangilikka aloqador postlarlar"),
                                          related_name="connected_faculty_dact", blank=True)
    departments = models.ManyToManyField("Departments",
                                         verbose_name=_("Yangilikka aloqadorlar kafedralar"),
                                         related_name="connected_departments", blank=True)
    section_and_centers = models.ManyToManyField(sections_and_centers.SectionsAndCenters,
                                                 verbose_name=_("Yangilikka aloqadorlar bo'lim va markazlar"),
                                                 related_name="connected_section_and_centers", blank=True)
    hashtag = models.ManyToManyField(widgets.Hashtag, related_name="news_hashtags", blank=True)
    brm = models.ManyToManyField(widgets.BRMItems, related_name="news_brm_items",
                                 verbose_name="Barqaror rivojlanish maqsadlari", blank=True)
    pdf_file = models.FileField(
        verbose_name=_("PDF fayl"), upload_to="pdf/news/%Y-%m-%d/",
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    pdf_file_en = models.FileField(
        verbose_name=_("EN PDF fayl"), upload_to="pdf/en/news/%Y-%m-%d/",
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    pdf_file_ru = models.FileField(
        verbose_name=_("RU PDF fayl"), upload_to="pdf/ru/news/%Y-%m-%d/",
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    video_file = models.FileField(
        verbose_name=_("Video fayl"), upload_to="videos/news/%Y-%m-%d/",
        null=True, blank=True, help_text=_("agar video fayl mavjud bo'lsa yuklang.")
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="author_news")
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name="update_news_user")

    class Meta:
        db_table = "news"
        managed = True
        verbose_name = _("Yangiliklar")
        verbose_name_plural = _("Yangiliklar")

    def __str__(self):
        return str(self.title)

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


class Ads(widgets.AbstractTemplate):
    """ model for ads """
    hashtag = models.ManyToManyField(widgets.Hashtag, related_name="ads_hashtags")
    pdf_file = models.FileField(
        verbose_name=_("PDF fayl"), upload_to="pdf/ads/%Y-%m-%d/",
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    pdf_file_en = models.FileField(
        verbose_name=_("EN PDF fayl"), upload_to="pdf/en/ads/%Y-%m-%d/",
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    pdf_file_ru = models.FileField(
        verbose_name=_("RU PDF fayl"), upload_to="pdf/ru/ads/%Y-%m-%d/",
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    video_file = models.FileField(
        verbose_name=_("Video fayl"), upload_to="videos/ads/%Y-%m-%d/",
        null=True, blank=True, help_text=_("agar video fayl mavjud bo'lsa yuklang.")
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="author_ads")
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="update_ads_user")

    class Meta:
        db_table = "ads"
        managed = True
        verbose_name = _("E'lonlar")
        verbose_name_plural = _("E'lonlar")

    def __str__(self):
        return str(self.title) if self.title else None

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


class VideoGallery(models.Model):
    """ video gallery model """
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("Author"),
                               related_name="video_author")
    title = models.CharField(max_length=255, verbose_name=_("Sarlavha"), null=True)
    status = models.CharField(_("Status"), choices=widgets.Status.choices, default=widgets.Status.pendding,
                              max_length=50)
    poster = models.ImageField(verbose_name=_("video uchun foster"), default="default/default.png", null=True,
                               upload_to="video/poster/%Y-%m-%d/")
    post = QuillField(verbose_name="Video file", null=True, blank=True)
    slug = models.SlugField(unique=True, verbose_name=_("Slug"), help_text=_("Majburyat tug'ulmasa tegmang"),
                            max_length=50)
    post_viewed_count = models.IntegerField(default=0, verbose_name=_("Ko'rilganlik soni"), help_text=_("Tegilmasin !"))
    added_at = models.DateTimeField(_("Vaqt & sana"))
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "videos_gallary"
        managed = True
        verbose_name = _("Video Galareya")
        verbose_name_plural = _("Video Galareya")

    def __str__(self):
        return f"{self.title}"


class Events(widgets.AbstractTemplate):
    """ university events plans """
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("Author"),
                               related_name="event_author")
    event_type = models.ForeignKey(widgets.EventTypes, on_delete=models.SET_NULL, null=True,
                                   verbose_name=_("Tadbir turini tanlang."))
    location = models.CharField(verbose_name=_("Tadbir manzili"), max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name=_("Bog'lanish uchun telefon raqam"), null=True, blank=True)
    extra_phone = models.CharField(max_length=20, verbose_name=_("Qo'shimcha telefon raqam"), null=True, blank=True)
    pdf_file = models.FileField(
        verbose_name=_("PDF fayl"), upload_to="pdf/news/%Y-%m-%d/",
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    pdf_file_en = models.FileField(
        verbose_name=_("EN PDF fayl"), upload_to="pdf/en/news/%Y-%m-%d/",
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    pdf_file_ru = models.FileField(
        verbose_name=_("RU PDF fayl"), upload_to="pdf/ru/news/%Y-%m-%d/",
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    video_file = models.FileField(
        verbose_name=_("Video fayl"), upload_to="videos/news/%Y-%m-%d/",
        null=True, blank=True, help_text=_("agar video fayl mavjud bo'lsa yuklang.")
    )
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="update_events_user")
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'events'
        managed = True
        verbose_name = _("Tadbirlar")
        verbose_name_plural = _("Tadbirlar")

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


class PhotoGallary(models.Model):
    """ photos model """
    news = models.ForeignKey(News, verbose_name=_("Yangilik"), on_delete=models.SET_NULL, null=True)
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
