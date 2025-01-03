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
    status = models.CharField(verbose_name=_("status"), max_length=30, choices=widgets.NavbarStatus.choices,
                              default=widgets.NavbarStatus.inside)
    order_num = models.IntegerField(verbose_name=_("Tartib raqami"), default=0)
    inside_order_num = models.IntegerField(default=0, verbose_name=_("Ichki tartib raqam"))
    slug = models.SlugField(max_length=120, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=255, null=True, blank=True, help_text="Tegish shart emas")
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="update_navbar_user")
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ("inside_order_num",)
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
    navbar = TreeForeignKey(to=Navbar, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Bo'lim nomi"))
    pdf_file = models.FileField(
        verbose_name=_("PDF fayl"), upload_to="pdf/posts/%Y-%m-%d/",
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    pdf_file_en = models.FileField(
        verbose_name=_("EN PDF file"), upload_to="pdf/en/posts/%Y-%m-%d/",
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    pdf_file_ru = models.FileField(
        verbose_name=_("RU PDF file"), upload_to="pdf/ru/posts/%Y-%m-%d/",
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    video_file = models.FileField(
        verbose_name=_("Video fayl"), upload_to="videos/posts/%Y-%m-%d/",
        null=True, blank=True, help_text=_("agar video fayl mavjud bo'lsa yuklang.")
    )
    faculty = models.BooleanField(default=False, verbose_name=_("Fakultet"),
                                  help_text=_("Agar shu post fakultet modeliga tegishli bo'lsa belgilang"))
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="update_post_user")
    zip_file = models.FileField(upload_to="zip_files/posts/%Y-%m-%d/",
                                null=True, blank=True, help_text=_("Faqat *.zip file yuklang"))

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
    image = models.ImageField(verbose_name=_("Hodim rasmi"), upload_to="image/facultyadministration/",
                              default="default/adminstrations.png")
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





class StudyProgram(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Yonalish nomi"), null=True)
    year = models.ForeignKey(widgets.Year, on_delete=models.SET_NULL, verbose_name=_("Yilni tanlang"), null=True)
    faculty = models.ForeignKey(Posts, on_delete=models.SET_NULL, null=True, verbose_name=_("Fakultetni tanlang"))
    department = models.ForeignKey("Departments", on_delete=models.SET_NULL, null=True,
                                   verbose_name=_("Kafedrani tanlang"))
    study_way = models.CharField(max_length=123, verbose_name=_("Ta'lim darajasini tanlang"),
                                 choices=widgets.StudyWayType.choices, default=widgets.StudyWayType.high)
    pdf_file = models.FileField(
        verbose_name=_("PDF fayl"), upload_to="pdf/study_program/%Y-%m-%d/", null=True, blank=True)
    pdf_file_en = models.FileField(
        verbose_name=_("EN PDF fayl"), upload_to="pdf/en/study_program/%Y-%m-%d/", null=True, blank=True)
    pdf_file_ru = models.FileField(
        verbose_name=_("RU PDF fayl"), upload_to="pdf/ru/study_program/%Y-%m-%d/", null=True, blank=True)
    study_time = models.CharField(max_length=123, verbose_name=_("O'qish vaqtlari"), choices=widgets.StudyTimes.choices,
                                  default=widgets.StudyTimes.daytime)
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
    image = models.ImageField(verbose_name=_("Rasm"), default="default/default.png",
                              upload_to="image/contact/%Y-%m-%d/", null=True)
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


class SocialNetworksBoss(models.Model):
    from colorfield.fields import ColorField
    name = models.CharField(max_length=255, verbose_name=_("Nomi"), null=True, blank=True)
    icon = models.CharField(max_length=255, verbose_name=_("Icon"), null=True, blank=True)
    color = ColorField(verbose_name=_("rangi"), null=True, blank=True, default="#123456")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'social_networks_boss'
        verbose_name = _("Ijtimoiy tarmoqlar Xodimlar")
        verbose_name_plural = _("Ijtimoiy tarmoqlar Xodimlar")


class UniversityAdmistrations(models.Model):
    """ university admistrations model """
    navbar = TreeForeignKey(to=Navbar, on_delete=models.SET_NULL, null=True, verbose_name=_("Bo'lim nomi"))
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


class UniversityAdministrationsImages(models.Model):
    administration = models.ForeignKey(to=UniversityAdmistrations, on_delete=models.SET_NULL, null=True,
                                       related_name="administration_images")
    image = models.ImageField(verbose_name=_("Rasmi"), upload_to="image/administrations/%Y-%m-%d/")

    class Meta:
        db_table = "administration_images"
        ordering = ["administration"]
        verbose_name = _("Insitut raxbariyati rasmlari")
        verbose_name_plural = _("Insitut raxbariyati rasmlari")

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


class NetworksBoss(models.Model):
    boss = models.ForeignKey(UniversityAdmistrations,
                             on_delete=models.SET_NULL, related_name="boss_network", null=True, blank=True)
    social_networks = models.ForeignKey(SocialNetworksBoss, models.SET_NULL, null=True, blank=True)
    url = models.CharField(max_length=255, verbose_name=_("URL"), null=True, blank=True)

    class Meta:
        db_table = 'networks_boss'
        verbose_name = _("Rahbariat ijtimoiy tarmoqlar")
        verbose_name_plural = _("Rahbariat ijtimoiy tarmoqlar")


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


class SectionsBoss(models.Model):
    post = models.ForeignKey(Posts, verbose_name=_("post"), on_delete=models.SET_NULL, related_name="sections_boss",
                             null=True)
    image = models.ImageField(_("Rasmi"), upload_to="image/boss_section/%Y-%m-%d/", null=True)
    position = models.ForeignKey(widgets.Positions, on_delete=models.SET_NULL,
                                 verbose_name=_("Lavozimi"), null=True, blank=True)
    f_name = models.CharField(_("To'liq ismi"), max_length=150)
    email = models.CharField(_("Email"), max_length=250)
    order_num = models.IntegerField(default=0)
    phone = models.CharField(_("Telefon raqami"), max_length=250)

    def __str__(self):
        return self.f_name

    class Meta:
        db_table = 'sections_bosses'
        ordering = ("order_num",)
        verbose_name = _("Bo'lim raxbarlari")
        verbose_name_plural = _("Bo'lim raxbarlari")


class StudyDegrees(models.Model):
    """ students degree bachelor, phd """
    name = models.CharField(max_length=123, blank=True, null=True, verbose_name=_("Nomi"))
    order_num = models.PositiveIntegerField(default=0, verbose_name=_("Tartib raqam"))
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        managed = True
        ordering = ("order_num",)
        db_table = 'study_degrees'
        verbose_name = _("Ta'lim darajalari")
        verbose_name_plural = _("Ta'lim darajalari")


class FieldOfEducation(models.Model):
    """ ta'lim sohasi """
    study_degree = models.ForeignKey(StudyDegrees, verbose_name=_("Ta'lim darajasini tanlang"),
                                     on_delete=models.SET_NULL, null=True)
    name = models.CharField(verbose_name=_("Nomi"), max_length=250, null=True)
    code = models.CharField(_("Ta'lim sohasi kodi"), max_length=150, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'field_of_education'
        managed = True
        verbose_name = _("Ta'lim sohalari")
        verbose_name_plural = _("Ta'lim sohalari")


class LearningWay(models.Model):
    """ study ways """
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Nomi"))
    study_degree = models.ForeignKey(
        StudyDegrees, verbose_name=_("Ta'lim darajasi"), on_delete=models.SET_NULL, null=True)
    faculty = models.ForeignKey(
        Posts, on_delete=models.SET_NULL, related_name="education_area_faculty",
        null=True, blank=True, verbose_name=_("Fakultet")
    )
    fields_edu = models.ForeignKey(
        FieldOfEducation, on_delete=models.SET_NULL, null=True, verbose_name=_("Ta'lim sohasi"))
    image = models.ImageField(
        verbose_name=_("Asosiy rasm"), upload_to="image/%Y-%m-%d/", default="default/default.png", null=True)
    post = QuillField(verbose_name=_("Haqida"), null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.study_degree}|{self.fields_edu}|{self.name}"

    class Meta:
        db_table = 'learning_way'
        managed = True
        verbose_name = _("Yo'nashish bo'limlari")
        verbose_name_plural = _("Yo'nashish bo'limlari")


class EducationalAreas(models.Model):
    """ ta'lim yo'nalishlari """
    study_way = models.ForeignKey(LearningWay, on_delete=models.SET_NULL, null=True,
                                  verbose_name=_("Yo'nashish bo'limi"))
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Nomi"))
    desc = QuillField(verbose_name=_("Yo'nalish xaqida"), null=True)
    pdf_file = models.FileField(
        _("PDF fayl"), upload_to="pdf/educational_areas/%Y-%m-%d/", null=True, blank=True,
        help_text=_("Faqat *.pdf formatdagi faylarni yuklang"), max_length=255)
    pdf_file_en = models.FileField(
        _("EN PDF fayl"), upload_to="pdf/en/educational_areas/%Y-%m-%d/",
        help_text=_("Faqat *.pdf formatdagi faylarni yuklang"),
        max_length=255, null=True, blank=True)
    pdf_file_ru = models.FileField(
        _("RU PDF fayl"), upload_to="pdf/ru/educational_areas/%Y-%m-%d/",
        help_text=_("Faqat *.pdf formatdagi faylarni yuklang"),
        max_length=255, null=True, blank=True)
    application_procedure = QuillField(_("Ariza berish tartibi"), null=True)
    tuition_fee = QuillField(_("O'qish to'lovi xaqida"), null=True)
    phone = models.CharField(_("Telefon raqam"), max_length=20, null=True)
    extra_phone = models.CharField(_("Qo'shimcha Telefon raqam"), max_length=20, null=True)
    email = models.EmailField(_("E-Pochta"), max_length=100, null=True)
    address = models.CharField(_("Manzil"), max_length=150, null=True)
    you_may_become_image = models.ImageField(verbose_name=_("Rasm"), null=True, blank=True,
                                             upload_to="image/you_may_become_image")
    you_may_become = QuillField(_("Siz bo'lishingiz mumkun"), null=True)
    full_time_fee = models.IntegerField(default=0, verbose_name=_("Kantrakt miqdori"))
    dept_fee = models.IntegerField(default=0, verbose_name=_("Kredit miqdori"))
    post_viewed_count = models.IntegerField(default=0, verbose_name=_("Ko'rilganlik soni"), help_text=_("Tegilmasin !"))
    author_post = models.CharField(verbose_name=_("Muallifi"), max_length=300, default="TKTI axborot xizmati")

    phd_subject_program = models.FileField(
        upload_to="pdf/educational_areas/phd_subject_program/%Y/%m/", null=True, blank=True,
        verbose_name=_("'Ixtisoslik' fanlari bo'yicha imtihon dasturlari")
    )
    phd_special_subject_program = models.FileField(
        upload_to="pdf/educational_areas/phd_special_subject_program/%Y/%m/", null=True, blank=True,
        verbose_name=_("Mutaxassislik fanlaridan malakaviy va qo'shimcha imtihon dasturlari")
    )

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'educational_areas'
        managed = True
        verbose_name = _("Ta'lim yo'nalishlari")
        verbose_name_plural = _("Ta'lim yo'nalishlari")

    def save(self, *args, **kwargs):
        if self._state.adding:
            im = Image.open(self.you_may_become_image)
            im = im.convert('RGB')
            im = ImageOps.exif_transpose(im)
            im_io = BytesIO()
            im.save(im_io, 'JPEG', quality=25)
            filename = os.path.splitext(self.you_may_become_image.name)[0]
            filename = f"{filename}.jpg"
            new_image = File(im_io, name=filename)
            self.you_may_become_image = new_image
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


class TypeStudyProgram(models.TextChoices):
    DAY = "day", _("Kundizgi")
    EVENING = "evening", _("Kechki")
    EXTERNALLY = "externally", _("Sirtqi")
    MASTER = "master", _("Magistratura")
    PHD = "phd", _("PHD")
    DSc = "dsc", _("DSc")


class AboutStudyProgramPDF(models.Model):
    type = models.CharField(
        max_length=100, choices=TypeStudyProgram.choices,
        null=True, blank=True)
    education_area = models.ForeignKey(
        EducationalAreas, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="educational_area")
    pdf_file = models.FileField(
        _("PDF fayl"), upload_to="pdf/about_study_program_pdf/%Y/%m/%d/",
        help_text=_("Faqat *.pdf formatdagi faylarni yuklang"),
        max_length=255, null=True, blank=True)
    pdf_file_en = models.FileField(
        _("EN PDF fayl"), upload_to="pdf/en/about_study_program_pdf/%Y/%m/%d/",
        help_text=_("Faqat *.pdf formatdagi faylarni yuklang"),
        max_length=255, null=True, blank=True)
    pdf_file_ru = models.FileField(
        _("RU PDF fayl"), upload_to="pdf/ru/about_study_program_pdf/%Y/%m/%d/",
        help_text=_("Faqat *.pdf formatdagi faylarni yuklang"),
        max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.type} -> {self.education_area.name}"

    class Meta:
        ordering = ("education_area",)
        db_table = "about_study_program_pdf"
        verbose_name = _("Ta'lim yo'nalishlari xaqidagi pdf")
        verbose_name_plural = _("Ta'lim yo'nalishlari xaqidagi pdf")


class EntryRequirements(models.Model):
    type = models.CharField(
        max_length=100, choices=TypeStudyProgram.choices,
        null=True, blank=True)
    education_area = models.ForeignKey(
        EducationalAreas, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="educational_area_requirements")
    requirement = QuillField(null=True, blank=True, verbose_name=_("Kirish talablari"))
    full_time_fee = models.IntegerField(default=0, verbose_name=_("Kantrakt miqdori"))
    dept_fee = models.IntegerField(default=0, verbose_name=_("Kredit miqdori"))

    def __str__(self):
        return f"{self.type} - {self.education_area.name}"

    class Meta:
        ordering = ("-id",)
        db_table = "entry_requirements"
        verbose_name = _("Kirish talablari")
        verbose_name_plural = _("Kirish talablari")


class ThemesForEducation(models.Model):
    education_area = models.ForeignKey(
        EducationalAreas, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="education_areas_themes")
    name = models.CharField(max_length=255, verbose_name=_("Mavzu nomi"),
                            null=True, blank=True)
    desc = QuillField(null=True, blank=True, verbose_name=_("Haqida"))
    teacher = models.CharField(max_length=255, verbose_name=_("Ilmiy rahbar"),
                               null=True, blank=True)
    finance = models.CharField(max_length=255, verbose_name=_("Moliyalashtiruvi"),
                               null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ("added_at",)
        db_table = "themes_for_education"
        verbose_name = _("DSc va PHD Mavzulari")
        verbose_name_plural = _("DSc va PHD Mavzulari")


class ModuleOfStudyPrograme(models.Model):
    """ Module of the study programme by semesters """
    educational_area = models.ForeignKey(EducationalAreas, verbose_name=_("Ta'lim yo'nalishi"),
                                         on_delete=models.SET_NULL, null=True)
    semester = models.ForeignKey(widgets.Semesters, verbose_name=_("Semesterni tanlang"),
                                 on_delete=models.SET_NULL, null=True)
    name = models.CharField(_("Modul nomi"), max_length=250, null=True)
    pdf_file = models.FileField(_("PDF fayl"),
                                upload_to="pdf/modules_of_study_programe/%Y-%m-%d/", max_length=255)
    pdf_file_en = models.FileField(
        _("EN PDF fayl"), upload_to="pdf/en/modules_of_study_programe/%Y-%m-%d/", max_length=255, null=True, blank=True)
    pdf_file_ru = models.FileField(
        _("RU PDF fayl"), upload_to="pdf/ru/modules_of_study_programe/%Y-%m-%d/", max_length=255, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.semester}|{self.name}"

    class Meta:
        db_table = 'module_study_programes'
        managed = True
        verbose_name = _("Dars jadvallari")
        verbose_name_plural = _("Dars jadvallari")
