from django.db import models
from django.utils.translation import gettext_lazy as _

import main.models as my_model


class CertificatesThemes(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Nomi"), null=True, blank=True)

    class Meta:
        ordering = ('name',)
        db_table = 'certificates_themes'
        verbose_name = _("Malaka oshirish mavzulari")
        verbose_name_plural = _("Malaka oshirish mavzulari")

    def __str__(self):
        return str(self.name)


class Certificates(models.Model):
    year = models.ForeignKey(my_model.Year, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name=_("Malaka oshirish yili"))
    theme = models.ForeignKey(CertificatesThemes, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name=_("Mavzu"))
    f_name = models.CharField(max_length=255, verbose_name=_("F.I.SH"), null=True, blank=True)
    order = models.FileField(upload_to="pdf/certificates_order/%Y/%m/%d", null=True, blank=True,
                             verbose_name=_("Sertifikat buyrug'i"))
    certificate = models.FileField(upload_to="pdf/certificate/%Y/%m/%d", null=True, blank=True,
                                   verbose_name=_("Sertifikat"))
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'certificates'
        ordering = ('-add_time', )
        verbose_name = _("Malaka oshirish sertifikatlari")
        verbose_name_plural = _("Malaka oshirish sertifikatlar")

    def __str__(self):
        return str(self.f_name)

