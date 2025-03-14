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


class Positions(models.Model):
    name = models.CharField(unique=True, blank=True, null=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "positions"
        ordering = ("name",)
        verbose_name = _("Lavozimlar")
        verbose_name_plural = _("Lavozimlar")


class BaseVariables(models.Model):
    logo = models.ImageField(upload_to="image/logos/", blank=True, null=True)
    name = models.CharField(_("Nomi"), max_length=125, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=125, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    buses = models.CharField(max_length=125, blank=True, null=True)
    vacancy = models.CharField(max_length=125, blank=True, null=True)
    vacancy_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "base_variables"
        verbose_name = _("Asosiy o'zgaruvchilar")
        verbose_name_plural = _("Asosiy o'zgaruvchilar")


class TopNavbar(models.Model):
    name = models.CharField(_("Nomi"), max_length=255, blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)
    order_num = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "top_navbar"
        ordering = ("order_num",)
        verbose_name = _("Top Navbar")
        verbose_name_plural = _("Top Navbar")


class AbstractTemplate(models.Model):
    """ abstract template for news posts and ads """
    image = models.ImageField(verbose_name=_("Asosiy rasm"), upload_to="image/%Y-%m-%d/", blank=True, null=True)
    title = models.CharField(verbose_name=_("Sarlavha"), max_length=500, null=True)
    subtitle = models.CharField(verbose_name=_("Qisqacha mazmun"), max_length=255, null=True)
    post = QuillField(verbose_name=_("To'liq mazmuni"), null=True, blank=True)
    status = models.CharField(verbose_name=_("status"), max_length=50, choices=Status.choices, default=Status.pendding)
    slug = models.SlugField(max_length=50, verbose_name="slug", unique=True,
                            help_text=_("Majburyat tug'ulmasa tegmang"))
    post_viewed_count = models.IntegerField(default=0, verbose_name=_("Ko'rilganlik soni"), help_text=_("Tegilmasin !"))
    author_post = models.CharField(verbose_name=_("Muallifi"), max_length=300, default=_("TKTI axborot xizmati"))
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
    name = models.CharField(max_length=50, verbose_name=_("Nomi"),
                            unique=True, null=True,
                            help_text=_("ishtimoiy tarmoq nomlarini kiriting, m: facebook, instagram"))
    icon = models.CharField(
        max_length=50, verbose_name=_("Icon"), null=True,
        help_text=_(
            "messangerning icon class nomi, class nomlarini olish uchun https://fontawesome.com/v5/search shu saytga kiring, m: fab fa-facebook"))
    color = ColorField(verbose_name=_("rangi"), null=True)
    url = models.URLField(verbose_name=_("url manzil"))
    order_num = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    update_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="update_network_user")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'social_networks'
        managed = True
        verbose_name = _("Ijtimoiy tarmoqlar")
        verbose_name_plural = _("Ijtimoiy tarmoqlar")

    def __str__(self):
        return str(self.name)


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
            im.save(im_io, 'JPEG', quality=30)
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
    logo = models.ImageField(verbose_name=_("rasmi"), default="default/gerb.png",
                             null=True, blank=True, upload_to="image/usefull_links/%Y-%m-%d/")
    link = models.URLField(verbose_name=_("Saytga havola"), max_length=150)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "usefull_links"
        managed = True
        verbose_name = "Foydali havolalar"
        verbose_name_plural = "Foydali havolalar"

    def __str__(self):
        return str(self.name)


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
        return str(self.name)


class Statistika(models.Model):
    """ universitet xaqida statistik malumotlar """
    name = models.CharField(_("Nomi"), max_length=80, unique=True)
    icon = models.CharField(_("icon"), max_length=50, null=True)
    quantity = models.IntegerField(_("soni"), default=0)
    url = models.URLField(max_length=300, verbose_name="url manzil", null=True, blank=True)
    order_num = models.IntegerField(_("Tartib raqam"), default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "statistika"
        managed = True
        verbose_name = _("Statistika")
        verbose_name_plural = _("Statistika")

    def __str__(self):
        return self.name


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


class FaqCategory(models.Model):
    """ faq category model """
    name = models.CharField(max_length=255, verbose_name=_("Nomi"), blank=True, null=True)

    def __str__(self):
        return self.name


class EventTypes(models.Model):
    """ event types model """
    name = models.CharField(_("Nomi"), max_length=255, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'event_type'
        managed = True
        verbose_name = _("Tadbir turlari")
        verbose_name_plural = _("Tadbir turlari")


class Semesters(models.Model):
    """ semesterlar """
    name = models.CharField(max_length=123, blank=True, null=True, verbose_name=_("Nomi"))
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'semesters'
        managed = True
        ordering = ("name",)
        verbose_name = _("Semesterlar")
        verbose_name_plural = _("Semesterlar")


class Faq(models.Model):
    """ faq model (ko'p berilgan savollar) """
    from main.models import posts
    from mptt.models import TreeForeignKey
    category = TreeForeignKey(posts.Navbar, on_delete=models.SET_NULL, null=True, verbose_name=_("Bo'lim nomi"))
    title = models.CharField(_("Savol"), max_length=255, unique=True, null=True)
    answer = QuillField(_("Javob"), null=True, blank=True)
    is_active = models.BooleanField(_('Aktiv'), default=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'faq'
        managed = True
        verbose_name = _("Ko'p beriladigan savollar")
        verbose_name_plural = _("Ko'p beriladigan savollar")


class BRMItems(models.Model):
    """ BRM items model """
    name = models.CharField(max_length=255, verbose_name=_("Nomi"), null=True)
    desc = QuillField(null=True, blank=True, verbose_name=_("Xaqida"))
    number = models.IntegerField(default=0, verbose_name="Raqami")
    color = ColorField(null=True, verbose_name="Rangi", default="#FF0000")
    pdf_file = models.FileField(
        upload_to="pdf/brm_items/%d", null=True, blank=True)
    pdf_file_en = models.FileField(
        upload_to="pdf/en/brm_items/%d", null=True, blank=True)
    pdf_file_ru = models.FileField(
        upload_to="pdf/ru/brm_items/%d", null=True, blank=True)
    video_file = models.FileField(
        verbose_name=_("Video fayl"), upload_to="videos/brm_items/%d/",
        null=True, blank=True, help_text=_("agar video fayl mavjud bo'lsa yuklang.")
    )
    image = models.ImageField(verbose_name=_("Rasmi"), upload_to="image/brm/%Y-%m-%d/", null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'brm_items'
        managed = True
        verbose_name = _("BRM")
        verbose_name_plural = _("BRM")


class ExtraFile(models.Model):
    from main.models import posts
    post = models.ForeignKey(posts.Posts, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name="extra_file")
    brm_item = models.ForeignKey(BRMItems, on_delete=models.SET_NULL,
                                 related_name="brm_extra_file", null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="File nomi", null=True, blank=True)
    pdf_file = models.FileField(
        upload_to="pdf/extra_files/%Y/%m/%d", null=True, blank=True)
    pdf_file_en = models.FileField(
        upload_to="pdf/en/extra_files/%Y/%m/%d", null=True, blank=True)
    pdf_file_ru = models.FileField(
        upload_to="pdf/ru/extra_files/%Y/%m/%d", null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'extra_files'
        managed = True
        ordering = ["post"]
        verbose_name = _("Qo'shimcha PDF fayllar")
        verbose_name_plural = _("Qo'shimcha PDF fayllar")


class FinancialBenefit(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Nomi"), null=True, blank=True)
    icon = models.CharField(max_length=100, verbose_name=_("Icon"), null=True, blank=True)
    about = QuillField(verbose_name=_("Imtiyoz haqida"), null=True, blank=True)
    responsible_organization = models.CharField(max_length=255, verbose_name=_("Mas'ul tashkilot"), null=True,
                                                blank=True)
    for_who = QuillField(verbose_name=_("Kimlar uchun"), null=True, blank=True)
    deadline = QuillField(verbose_name=_("Imtiyozni taqdim etish tartibi va muddatlari"),
                          null=True, blank=True)
    main_lower = QuillField(verbose_name=_("Huquqiy asos"), null=True, blank=True)
    contact = QuillField(verbose_name=_("Aloqa ma’lumotlari"), null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'financial_benefits'
        verbose_name = _("Moliyaviy imtiyozlar")
        verbose_name_plural = _("Moliyaviy imtiyozlar")


class Digitization(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Nomi"), null=True, blank=True)
    icon = models.CharField(max_length=255, verbose_name=_("Icon"), null=True, blank=True)
    url = models.URLField(verbose_name=_("URL"), max_length=400, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'digitizations'
        verbose_name = _("Raqamlashtirish")
        verbose_name_plural = _("Raqamlashtirish")
