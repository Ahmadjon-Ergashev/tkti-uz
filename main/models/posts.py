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
        return self.name



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
        return f"{self.navbar} | {self.title[:30]}"
    
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
    about = QuillField(verbose_name=_("Xaqida"), null=True, blank=True)
    target = QuillField(verbose_name=_("Maqsad"), null=True, blank=True)
    activity = QuillField(verbose_name=_("Faoliyati"), null=True, blank=True)
    slug = models.SlugField(max_length=255, verbose_name=_("Slug"), null=True, help_text=_("Zarurat tug'ulmasa tegilmasin"), unique=True)
    post_viewed_count = models.IntegerField(_("Ko'rilganlik soni"), default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "departments"
        managed = True
        ordering = ["-added_at"]
        verbose_name = _("Kafedra")
        verbose_name_plural = _("Kafedralar")

    def __str__(self):
        return self.name


class DepartmentsAdmistrations(models.Model):
    """ adminstrations of departments """
    department = models.ForeignKey(Departments, verbose_name=_("Kafedrani tanglang"), on_delete=models.SET_NULL, null=True)
    image = models.ImageField(verbose_name=_("Hodim rasmi"), upload_to="image/departmentsadminstations/", default="default/adminstrations.png")
    f_name = models.CharField(verbose_name=_("To'liq ismi"), max_length=120, null=True)
    job_name = models.CharField(verbose_name=_("Mutaxasisligi"), max_length=120, null=True)
    admission_day = models.CharField(verbose_name=_("Qabul kunlari"), max_length=150, null=True)
    phone_number = models.CharField(verbose_name=_("Telefon raqami"), max_length=20, null=True)
    email = models.EmailField(verbose_name=_("E-Pochta manzili"), max_length=120, null=True)
    order_num = models.IntegerField(default=0, verbose_name=_("Tartib raqam"))
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.f_name
    
    class Meta:
        db_table = 'dept_adminstrations'
        managed = True
        ordering = ["order_num"]
        verbose_name = _("Kafedra ma'muryati")
        verbose_name_plural = _("Kafedra ma'muryati")



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
    

class ContactSection(models.Model):
    """ contact model """
    navbar = TreeForeignKey(to=Navbar, on_delete=models.SET_NULL, null=True, verbose_name=_("Bo'lim nomi"))
    title = models.CharField(_("Sarlavha"), max_length=250, null=True)
    image = models.ImageField(verbose_name=_("Rasm"), default="default/default.png", upload_to="image/contact/%Y-%m-%d/", null=True)
    email = models.EmailField(verbose_name=_("E-Pochta"), max_length=255, default="info@tkti.uz")
    phone = models.CharField(verbose_name=_("Telefon raqami"), max_length=17, null=True, help_text="+998332300701")
    address = models.CharField(verbose_name=_("Manzil"), max_length=250, null=True)
    address_url = models.URLField(_("E-Manzil"), max_length=200)
    order_num = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'contact_section'
        managed = True
        verbose_name = _("Bog'lanish")
        verbose_name_plural = _("Bog'lanish")

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


class Workers(models.Model):
    """ xodimlar """
    image = models.ImageField(verbose_name=_("Rasmi"), upload_to="image/workers/%Y-%m-%d/", default="default/adminstrations.png")
    position = models.CharField(_("Lavozimi"), choices=widgets.WorkerPositions.choices, default=widgets.WorkerPositions.department_head, max_length=150, null=True)
    f_name = models.CharField(_("To'liq ismi"), max_length=150, null=True)
    email = models.EmailField(verbose_name=_("E-Pochta"), max_length=255, null=True, help_text="example@domain.com")
    phone = models.CharField(verbose_name=_("Telefon raqami"), max_length=20, null=True, help_text="+998332300701")
    extra_phone = models.CharField(verbose_name=_("Qo'shimcha Telefon raqami"), max_length=20, null=True, blank=True, help_text="+998332300703")
    section = models.ForeignKey("SectionsAndCenters", verbose_name=_("Bo'lim va markaz nomi"), on_delete=models.SET_NULL, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.f_name} | {self.position} | {self.phone}"

    class Meta:
        db_table = 'workers_for_sections'
        managed = True
        verbose_name = _("Bo'lim va Markazlar xodimlari")
        verbose_name_plural = _("Bo'lim va Markazlar xodimlari") 


class SectionsAndCenters(models.Model):
    """ bo'lim va markazlar """
    navbar = TreeForeignKey(to=Navbar, on_delete=models.SET_NULL, null=True, verbose_name=_("Bo'lim nomi"))
    title = models.CharField(max_length=255, verbose_name=_("Sarlavha"), null=True)
    about = QuillField(verbose_name=_("Xaqida"), null=True)
    target = QuillField(verbose_name=_("Maqsad"), null=True)
    activity = QuillField(verbose_name=_("Faoliyati"), null=True, blank=True)
    slug = models.SlugField(_("Slug"), max_length=255, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'sections_and_centers'
        managed = True
        verbose_name = _("Bo'lim va Markazlar")
        verbose_name_plural = _("Bo'lim va Markazlar")

    
class UniversityAdmistrations(models.Model):
    """ university admistrations model """
    navbar = TreeForeignKey(to=Navbar, on_delete=models.SET_NULL, null=True, verbose_name=_("Bo'lim nomi"))
    image = models.ImageField(verbose_name=_("Rasmi"), upload_to="image/adminstrations/%Y-%m-%d/", default="default/adminstrations.png")
    f_name = models.CharField(_("To'liq ismi"), max_length=150, null=True)
    position = models.CharField(_("Lavozimi"), max_length=255, null=True)
    email = models.EmailField(verbose_name=_("E-Pochta"), max_length=255, null=True, help_text="example@domain.com")
    phone = models.CharField(verbose_name=_("Telefon raqami"), max_length=20, null=True, help_text="+998332300701")
    admission_days = models.CharField(verbose_name=_("Qabul vaqti"), max_length=255, null=True)
    short_info = QuillField(verbose_name=_("Qisqacha ma'lumot"), null=True)
    scientific_direction = QuillField(verbose_name=_("Ilmiy yo'nalishlari"), null=True)
    main_tasks_in_position = QuillField(verbose_name=_("Lavozimidagi asosiy vazifalar"), null=True)
    scientific_activity = QuillField(verbose_name=_("Ilmiy va pedagogik mehnat faoliyati"), null=True)
    facebook = models.URLField(_("Facebook manzili"), max_length=200, null=True, blank=True)
    instagram = models.URLField(_("Instagram manzili"), max_length=200, null=True, blank=True)
    linkedin = models.URLField(_("Linkedin manzili"), max_length=200, null=True, blank=True)
    order_num = models.IntegerField(default=0, verbose_name=_("Tartib raqami"))
    slug = models.SlugField(_("Slug"), null=True, blank=True)
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.f_name
    
    class Meta:
        db_table = 'university_admistration'
        managed = True
        ordering = ["order_num"]
        verbose_name = _("Insitut raxbariyati")
        verbose_name_plural = _("Insitut raxbariyati")

    def save(self, *args, **kwargs):
        if self._state.adding:
            im = Image.open(self.image)
            im = im.convert('RGB')
            im = ImageOps.exif_transpose(im)
            im_io = BytesIO()
            im.save(im_io, 'JPEG', quality=25)
            filename = os.path.splitext(self.image.name)[0]
            filename = f"{filename}.jpg"
            new_image = File(im_io, name=filename)
            self.image = new_image
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


class TalentedStudents(models.Model):
    """ talented students in university """
    image = models.ImageField(verbose_name=_("Rasmi"), upload_to="image/students/%Y-%m-%d/", null=True)
    f_name = models.CharField(_("To'liq ismi"), max_length=150, null=True)
    desc = models.TextField(_("Ta'laba xaqida"), null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.f_name

    class Meta:
        db_table = 'talanted_students'
        managed = True
        verbose_name = _("Iqtidorli talabalar")
        verbose_name_plural = _("Iqtidorli talabalar")    
    

class BossSection(models.Model):
    post = models.ForeignKey(Posts, verbose_name=_("post"), on_delete=models.SET_NULL, null=True)
    image = models.ImageField(_("Rasmi"), upload_to="image/boss_section/%Y-%m-%d/", null=True)
    position = models.CharField(
        max_length=255, verbose_name=_("Lavozimi"), 
        choices=widgets.WorkerPositions.choices, default=widgets.WorkerPositions.department_head)
    f_name = models.CharField(_("To'liq ismi"), max_length=150)
    email = models.CharField(_("Email"), max_length=250)
    phone = models.CharField(_("Telefon raqami"), max_length=250)

    def __str__(self):
        return self.f_name
    

class StudyDegrees(models.Model):
    """ students degree bachelor, phd """
    name = models.CharField(max_length=123, blank=True, null=True, verbose_name=_("Nomi"))
    faculty = models.ManyToManyField(Posts, related_name="students_degree_faculty")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'study_degrees'
        managed = True
        verbose_name = _("Ta'lim darajalari")
        verbose_name_plural = _("Ta'lim darajalari")


class LearningWay(models.Model):
    """ study ways """
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Nomi"))
    study_degree = models.ForeignKey(StudyDegrees, verbose_name=_("Ta'lim darajasi"), on_delete=models.SET_NULL, null=True)
    faculty = models.ForeignKey(Posts, verbose_name=_("Fakultet nomi"), on_delete=models.SET_NULL, null=True)
    image = models.ImageField(verbose_name=_("Asosiy rasm"), upload_to="image/%Y-%m-%d/", default="default/default.png", null=True)
    post = QuillField(verbose_name=_("Xaqida"), null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.study_degree}|{self.faculty}|{self.name}"

    class Meta:
        db_table = 'learning_way'
        managed = True
        verbose_name = _("Yo'nashish bo'limlari")
        verbose_name_plural = _("Yo'nashish bo'limlari")


class EducationalAreas(models.Model):
    """ ta'lim yo'nalishlari """
    study_way = models.ForeignKey(LearningWay, on_delete=models.SET_NULL, null=True, verbose_name=_("Yo'nashish bo'limi"))
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Nomi"))
    desc = QuillField(verbose_name=_("Yo'nalish xaqida"), null=True)
    pdf_file = models.FileField(
        _("PDF fayl"), upload_to="pdf/educational_areas/%Y-%m-%d/", 
        help_text=_("Faqat *.pdf formatdagi faylarni yuklang"), max_length=255)
    application_procedure = QuillField(_("Ariza berish tartibi"), null=True)
    tuition_fee = QuillField(_("O'qish to'lovi xaqida"), null=True)
    contact = QuillField(_("Bog'lanish"), null=True)
    you_may_become = QuillField(_("Siz bo'lishingiz mumkun"), null=True)
    full_time_fee = models.IntegerField(default=0, verbose_name=_("Kundizgi ta'lim uchun"))
    full_time_night_fee = models.IntegerField(default=0, verbose_name=_("Kechgi ta'lim uchun"))
    full_time_external_fee = models.IntegerField(default=0, verbose_name=_("Sirtqi ta'lim uchun"))
    post_viewed_count = models.IntegerField(default=0, verbose_name=_("Ko'rilganlik soni"), help_text=_("Tegilmasin !"))
    author_post = models.CharField(verbose_name=_("Muallifi"), max_length=300, default="TKTI axborot xizmati")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'educational_areas'
        managed = True
        verbose_name = _("Ta'lim yo'nalishlari")
        verbose_name_plural = _("Ta'lim yo'nalishlari")



class ModuleOfStudyPrograme(models.Model):
    """ Module of the study programme by semesters """
    educational_area = models.ForeignKey(EducationalAreas, verbose_name=_("Ta'lim yo'nalishi"), on_delete=models.SET_NULL, null=True)
    semester = models.ForeignKey(widgets.Semesters, verbose_name=_("Semesterni tanlang"), on_delete=models.SET_NULL, null=True)
    name = models.CharField(_("Modul nomi"), max_length=250, null=True)
    pdf_file = models.FileField(_("PDF fayl"), upload_to="pdf/modules_of_study_programe/%Y-%m-%d/", max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.semester}|{self.name}"

    class Meta:
        db_table = 'module_study_programes'
        managed = True
        verbose_name = _("Dars jadvallari")
        verbose_name_plural = _("Dars jadvallari")






    

    

