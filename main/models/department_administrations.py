from django.db import models
import main.models as local_models
from django.utils.translation import gettext_lazy as _


class DepartmentHeadAdministrations(models.Model):
    """ KAFEDRA MUDIRLARI RO'YHATI """
    department = models.ForeignKey(
        local_models.Departments, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='department_head_administration')
    image = models.ImageField(
        verbose_name=_("Rasm"), upload_to="department_head_administrations/%Y/%m/%d", blank=True, null=True)
    f_name = models.CharField(max_length=150, verbose_name=_("To'liq ismi"), blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name=_("E-Pochta"))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Telefon raqami"))
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.f_name)

    class Meta:
        db_table = 'department_head_administrations'
        ordering = ('-id',)
        verbose_name = _("Kafedra mudirlari")
        verbose_name_plural = _("Kafedra mudirlari")


class DepartmentAdministrationsPositions(models.Model):
    """ KAFEDRA ISHCHILARINING LAVOZIMLARI """
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name=_("Nomi"))
    order_num = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'department_administrations_positions'
        ordering = ('order_num',)
        verbose_name = _("Kafedra mamuryati lavozimlari")
        verbose_name_plural = _("Kafedra mamuryati lavozimlari")


class DepartmentAdministrationsNew(models.Model):
    """ KAFEDRA MAMURYATI RO'YHATI '"""
    position = models.ForeignKey(DepartmentAdministrationsPositions, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='department_administrations_positions', verbose_name=_("Lavozim"))
    department = models.ForeignKey(local_models.Departments, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name=_("Kafedra"), related_name="department_administrations")
    f_name = models.CharField(max_length=150, verbose_name=_("To'liq ismi"), null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True, verbose_name=_("E-Pochta"))
    cv = models.FileField(
        verbose_name=_("CV File"), null=True, blank=True,
        upload_to="department_administration_cv/%Y/%m/%d")

    def __str__(self):
        return str(self.f_name)

    class Meta:
        ordering = ('position',)
        db_table = 'department_administrations_new'
        verbose_name = _("Kafedra mamuryati (yangi)")
        verbose_name_plural = _("Kafedra mamuryati (yangi)")
