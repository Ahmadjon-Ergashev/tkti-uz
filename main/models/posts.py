import os
from io import BytesIO
from django.db import models
from PIL import Image, ImageOps
from django.core.files import File
from django_quill.fields import QuillField
from django.contrib.auth.models import User
from mptt.models import TreeForeignKey, MPTTModel
from django.utils.translation import gettext_lazy as _


# local
from main.models import widgets


class Navbar(MPTTModel):
    """ Navigation bar model """
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, 
        verbose_name=_("object_make_user"), related_name="navbar_author"
    )
    name = models.CharField(verbose_name=_("Nomi"), max_length=100)
    parent = TreeForeignKey("self", related_name="children", on_delete=models.SET_NULL, null=True, blank=True)
    visible = models.BooleanField(default=True, verbose_name=_("Ko'rinish"))
    status = models.CharField(verbose_name=_("status"), max_length=30, choices=widgets.NavbarStatus.choices, default=widgets.NavbarStatus.inside)
    order_num = models.IntegerField(verbose_name=_("Tartib raqami"), default=0)
    inside_order_num = models.IntegerField(default=0, verbose_name=_("Ichki tartib raqam"))
    slug = models.SlugField(max_length=120, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="update_navbar_user")
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ("inside_order_num", )
        added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "navbar"
        managed = True
        verbose_name = _("Bo'limlar")
        verbose_name_plural = _("Bo'limlar")


    def __str__(self):
        return str(self.name) if self.name else None



class Posts(widgets.AbstractTemplate):
    """ Posts """
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, 
        verbose_name=_("object_make_user"), related_name="post_author"
    )
    navbar = TreeForeignKey(to=Navbar, on_delete=models.SET_NULL, null=True, verbose_name=_("Bo'lim nomi"))
    pdf_file = models.FileField(
        verbose_name=_("PDF fayl"), upload_to="pdf/posts/%Y-%m-%d/", 
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    video_file = models.FileField(
        verbose_name=_("Video fayl"), upload_to="videos/posts/%Y-%m-%d/",
        null=True, blank=True, help_text=_("agar video fayl mavjud bo'lsa yuklang.")
    )
    faculty = models.BooleanField(default=False, verbose_name=_("Fakultet"), help_text=_("Agar shu post fakultet modeliga tegishli bo'lsa belgilang"))
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="update_post_user")
    
    class Meta:
        db_table = "posts"
        managed = True
        verbose_name = _("Postlar")
        verbose_name_plural = _("Postlar")

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



class FacultyAdministration(models.Model): 
    """ model for faculty admistrations """
    faculty = models.ForeignKey(Posts, on_delete=models.SET_NULL, null=True, verbose_name=_("Fakultet nomi"))
    image = models.ImageField(verbose_name=_("Hodim rasmi"), upload_to="image/facultyadministration/", default="default/adminstrations.png")
    f_name = models.CharField(verbose_name=_("To'liq ismi"), max_length=120, null=True)
    job_name = models.CharField(verbose_name=_("Mutaxasisligi"), max_length=120, null=True)
    admission_day = models.CharField(verbose_name=_("Qabul kunlari"), max_length=150, null=True)
    phone_number = models.CharField(verbose_name=_("Telefon raqami"), max_length=20, null=True)
    email = models.EmailField(verbose_name=_("E-Pochta manzili"), max_length=120, null=True)
    order_num = models.IntegerField(default=0, verbose_name=_("Tartib raqam"))
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "faculty_adminstration"
        managed = True
        ordering = ["order_num"]
        verbose_name = _("Fakultet ma'muryati")
        verbose_name_plural = _("Fakultet ma'muryati")

    def __str__(self):
        return f"{self.f_name} | {self.job_name}"


class Departments(models.Model):
    """ model for departments of faculty (kafedra)"""
    name = models.CharField(_("Kafedra nomi"), max_length=150, null=True)
    faculty = models.ForeignKey(Posts, on_delete=models.SET_NULL, null=True, verbose_name=_("Fakultet nomi"))
    pdf_file = models.FileField(verbose_name=_("PDF fayl"), help_text=_("Faqat PDF formatidagi faylni joylang"), null=True, blank=True, upload_to="pdf/departments/%Y-%m-%d/")
    post = QuillField(null=True, blank=True, verbose_name=_("To'liq matn"))
    slug = models.SlugField(max_length=255, verbose_name=_("Slug"), null=True, help_text=_("Zarurat tug'ulmasa tegilmasin"), unique=True)
    post_viewed_count = models.IntegerField(_("Ko'rilganlik soni"), default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "departments"
        managed = True
        verbose_name = _("Kafedra")
        verbose_name_plural = _("Kafedralar")

    def __str__(self):
        return self.name


class StudyProgram(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Yonalish nomi"), null=True)
    year = models.ForeignKey(widgets.Year, on_delete=models.SET_NULL, verbose_name=_("Yilni tanlang"), null=True)
    faculty = models.ForeignKey(Posts, on_delete=models.SET_NULL, null=True, verbose_name=_("Fakultetni tanlang"))
    department = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True, verbose_name=_("Kafedrani tanlang"))
    study_way = models.CharField(max_length=123, verbose_name=_("Ta'lim darajasini tanlang"), choices=widgets.StudyWayType.choices, default=widgets.StudyWayType.high)
    pdf_file = models.FileField(verbose_name=_("PDF fayl"), upload_to="pdf/study_program/%Y-%m-%d/")
    study_time = models.CharField(max_length=123, verbose_name=_("O'qish vaqtlari"), choices=widgets.StudyTimes.choices, default=widgets.StudyTimes.daytime)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'study_program'
        managed = True
        verbose_name = _("Ta'lim dasturi katalogi")
        verbose_name_plural = _("Ta'lim dasturi katalogi")
    
    def __str__(self):
        return f"{self.year}|{self.faculty.title}|{self.department.name}|{self.study_way}"