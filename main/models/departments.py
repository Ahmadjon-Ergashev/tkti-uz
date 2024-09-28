from django.db import models
from django_quill.fields import QuillField
from django.utils.translation import gettext_lazy as _


class Departments(models.Model):
    """ model for departments of faculty (kafedra) """
    name = models.CharField(_("Kafedra nomi"), max_length=150, null=True)
    faculty = models.ForeignKey("Posts", on_delete=models.SET_NULL, null=True, verbose_name=_("Fakultet nomi"))
    pdf_file = models.FileField(
        verbose_name=_("PDF fayl"), help_text=_("Faqat PDF formatidagi faylni joylang"),
        null=True, blank=True, upload_to="pdf/departments/%Y-%m-%d/")
    pdf_file_en = models.FileField(
        verbose_name=_("EN PDF fayl"), help_text=_("Faqat PDF formatidagi faylni joylang"),
        null=True, blank=True, upload_to="pdf/en/departments/%Y-%m-%d/")
    pdf_file_ru = models.FileField(
        verbose_name=_("RU PDF fayl"), help_text=_("Faqat PDF formatidagi faylni joylang"),
        null=True, blank=True, upload_to="pdf/ru/departments/%Y-%m-%d/")
    about = QuillField(verbose_name=_("Haqida"), null=True, blank=True)
    target = QuillField(verbose_name=_("Maqsad"), null=True, blank=True)
    activity = QuillField(verbose_name=_("Faoliyati"), null=True, blank=True)
    slug = models.SlugField(max_length=255, verbose_name=_("Slug"), null=True,
                            help_text=_("Zarurat tug'ulmasa tegilmasin"), unique=True)
    post_viewed_count = models.IntegerField(_("Ko'rilganlik soni"), default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    zip_file = models.FileField(upload_to="zip_files/posts/%Y-%m-%d/",
                                null=True, blank=True, help_text=_("Faqat *.zip, *.docx, *.excel turdagi file yuklang"))

    class Meta:
        db_table = "departments"
        managed = True
        ordering = ["-added_at"]
        verbose_name = _("Kafedra")
        verbose_name_plural = _("Kafedralar")

    def __str__(self):
        return self.name


class DepartmentCharterDocument(models.Model):
    department = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="department_charter_files")
    department_charter = models.FileField(upload_to="pdf/department_files/charter/uz/%Y-%m-%d/", null=True, blank=True,
                                          verbose_name="Kafedra nizomi")
    department_charter_en = models.FileField(upload_to="pdf/department_files/charter/en/%Y-%m-%d/", null=True,
                                             blank=True,
                                             verbose_name="Department Charter")

    department_charter_ru = models.FileField(upload_to="pdf/department_files/charter/ru/%Y-%m-%d/", null=True,
                                             blank=True,
                                             verbose_name="Устав кафедры")

    def __str__(self):
        return str(self.department.name)

    class Meta:
        db_table = "department_charter_files_table"
        managed = True
        verbose_name = _("Kafedra nizomi")
        verbose_name_plural = _("Kafedra nizomi")


class DepartmentPlanDocument(models.Model):
    department = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="department_plan_files")

    department_plan = models.FileField(upload_to="pdf/department_files/plan/uz/%Y-%m-%d/", null=True, blank=True,
                                       verbose_name="Kafedra rejasi")

    department_plan_en = models.FileField(upload_to="pdf/department_files/plan/en/%Y-%m-%d/", null=True, blank=True,
                                          verbose_name="Department plan")

    department_plan_ru = models.FileField(upload_to="pdf/department_files/plan/ru/%Y-%m-%d/", null=True, blank=True,
                                          verbose_name="План отдела")

    def __str__(self):
        return str(self.department.name)

    class Meta:
        db_table = "department_plan_files_table"
        managed = True
        verbose_name = _("Kafedra rejasi")
        verbose_name_plural = _("Kafedra rejasi")


class DepartmentsAdmistrations(models.Model):
    """ administrations of departments """
    department = models.ForeignKey(Departments, verbose_name=_("Kafedrani tanglang"), on_delete=models.SET_NULL,
                                   null=True)
    image = models.ImageField(verbose_name=_("Hodim rasmi"), upload_to="image/departmentsadminstations/",
                              default="default/adminstrations.png")
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
