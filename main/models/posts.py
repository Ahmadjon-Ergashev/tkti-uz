from django.db import models
from django_quill.fields import QuillField
from django.contrib.auth.models import User
from mptt.models import TreeForeignKey, MPTTModel
from django.utils.translation import gettext_lazy as _


class NavbarStatus(models.TextChoices):
    base = "base", _("Asosiy")
    inside = "inside", _("Ichki")


class Navbar(MPTTModel):
    """ Navigation bar model """
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, 
        verbose_name=_("object_make_user"), related_name="navbar_author"
    )
    name = models.CharField(verbose_name=_("Nomi"), max_length=100)
    parent = TreeForeignKey("self", related_name="children", on_delete=models.SET_NULL, null=True, blank=True)
    visible = models.BooleanField(default=True, verbose_name=_("Ko'rinish"))
    status = models.CharField(verbose_name=_("status"), max_length=30, choices=NavbarStatus.choices, default=NavbarStatus.inside)
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


class Status(models.TextChoices):
    published: str = "pub", _("Published")
    pendding: str = "pen", _("Pendding")


class Posts(models.Model):
    """ Posts """
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, 
        verbose_name=_("object_make_user"), related_name="post_author"
    )
    navbar = TreeForeignKey(to=Navbar, on_delete=models.SET_NULL, null=True, verbose_name=_("Bo'lim nomi"))
    image = models.ImageField(verbose_name=_("Post uchun asosiy rasm"), upload_to="posts/images/%Y-%m-%d/", null=True)
    title = models.CharField(verbose_name=_("Sarlovha"), max_length=400, null=True)
    subtitle = models.CharField(verbose_name=_("Qisqacha mazmun"), max_length=500, null=True)
    post = QuillField(null=True)
    pdf_file = models.FileField(
        verbose_name=_("PDF fayl"), upload_to="posts/pdf-files/%Y-%m-%d/", 
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    video_file = models.FileField(
        verbose_name=_("Video fayl"), upload_to="posts/videos/%Y-%m-%d/",
        null=True, blank=True, help_text=_("agar video fayl mavjud bo'lsa yuklang.")
    )
    status = models.CharField(verbose_name=_("post status"), max_length=50, choices=Status.choices, default=Status.pendding)
    slug = models.SlugField(max_length=255, verbose_name="slug", help_text=_("Majburyat tug'ulmasa tegmang"))
    post_viewed_count = models.IntegerField(default=0, verbose_name=_("Ko'rilganlik soni"), help_text=_("Tegilmasin !"))
    author_post = models.CharField(verbose_name=_("Post muallifi"), max_length=300, default="TKTI axborot xizmati")
    added_at = models.DateTimeField(verbose_name=_("Vaqt & sana"))
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="update_post_user")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "posts"
        managed = True
        verbose_name = "Postlar"
        verbose_name_plural = "Postlar"

    def __str__(self):
        return str(self.title) if self.title else None
    
    
    
