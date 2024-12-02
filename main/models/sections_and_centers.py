from django.db import models
from mptt.models import TreeForeignKey
from django_quill.fields import QuillField
from django.utils.translation import gettext_lazy as _

# local
from main.models import posts
from main.models import widgets


class Workers(models.Model):
    """ xodimlar """
    image = models.ImageField(verbose_name=_("Rasmi"), upload_to="image/workers/%Y-%m-%d/",
                              default="default/adminstrations.png")
    position = models.CharField(_("Lavozimi"), choices=widgets.WorkerPositions.choices,
                                default=widgets.WorkerPositions.department_head, max_length=150, null=True)
    self_position = models.ForeignKey(widgets.Positions, on_delete=models.SET_NULL,
                                      verbose_name=_("Lavozimi"), null=True, blank=True)
    f_name = models.CharField(_("To'liq ismi"), max_length=150, null=True)
    email = models.EmailField(verbose_name=_("E-Pochta"), max_length=255, null=True, help_text="example@domain.com")
    phone = models.CharField(verbose_name=_("Telefon raqami"), max_length=20, null=True, help_text="+998332300701")
    extra_phone = models.CharField(verbose_name=_("Qo'shimcha Telefon raqami"), max_length=20, null=True, blank=True,
                                   help_text="+998332300703")
    section = models.ForeignKey("SectionsAndCenters", verbose_name=_("Bo'lim va markaz nomi"),
                                on_delete=models.SET_NULL, null=True, blank=True)
    order_num = models.PositiveIntegerField(default=0, verbose_name=_("Tartib raqam"))
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.f_name} | {self.position} | {self.phone}"

    class Meta:
        managed = True
        ordering = ('order_num',)
        db_table = 'workers_for_sections'
        verbose_name = _("Bo'lim va Markazlar xodimlari")
        verbose_name_plural = _("Bo'lim va Markazlar xodimlari")


class SectionsAndCenters(models.Model):
    """ bo'lim va markazlar """
    image = models.ImageField(upload_to="image/sections_and_centers/", null=True, blank=True)
    navbar = TreeForeignKey(to=posts.Navbar, on_delete=models.SET_NULL, null=True, verbose_name=_("Bo'lim nomi"))
    title = models.CharField(max_length=255, verbose_name=_("Sarlavha"), null=True)
    about = QuillField(verbose_name=_("Xaqida"), null=True)
    target = QuillField(verbose_name=_("Maqsad"), null=True)
    activity = QuillField(verbose_name=_("Faoliyati"), null=True, blank=True)
    slug = models.SlugField(_("Slug"), max_length=255, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    zip_file = models.FileField(upload_to="zip_files/posts/%Y-%m-%d/",
                                null=True, blank=True, help_text=_("Faqat *.zip, *.docx, *.excel turdagi file yuklang"))

    pdf_file = models.FileField(
        verbose_name=_("PDF fayl"), upload_to="pdf/sections_and_centers/%Y-%m-%d/",
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    pdf_file_en = models.FileField(
        verbose_name=_("EN PDF file"), upload_to="pdf/en/sections_and_centers/%Y-%m-%d/",
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    pdf_file_ru = models.FileField(
        verbose_name=_("RU PDF file"), upload_to="pdf/ru/sections_and_centers/%Y-%m-%d/",
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'sections_and_centers'
        managed = True
        verbose_name = _("Bo'lim va Markazlar")
        verbose_name_plural = _("Bo'lim va Markazlar")
