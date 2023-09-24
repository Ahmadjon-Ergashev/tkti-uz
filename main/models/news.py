from django.db import models
from django_quill.fields import QuillField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

#local
from .posts import Status



class NewsAndAds(models.Model):
    """ model for news and announcement  """
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="author_news")
    image = models.ImageField(verbose_name=_("Asosiy rasm"), upload_to="news/images/%Y-%m-%d/", default="default/default.png", null=True)
    title = models.CharField(verbose_name=_("Sarlavha"), max_length=255, null=True)
    subtitle = models.CharField(verbose_name=_("Qisqacha mazmuni"), max_length=300, null=True)
    post = QuillField(verbose_name=_("To'liq mazmuni"), null=True)
    pdf_file = models.FileField(
        verbose_name=_("PDF fayl"), upload_to="news/pdf-files/%Y-%m-%d/", 
        null=True, blank=True, help_text=_("Faqat *.pdf formatdagi faylarni yuklang")
    )
    video_file = models.FileField(
        verbose_name=_("Video fayl"), upload_to="news/videos/%Y-%m-%d/",
        null=True, blank=True, help_text=_("agar video fayl mavjud bo'lsa yuklang.")
    )
    status = models.CharField(verbose_name=_("status"), max_length=50, choices=Status.choices, default=Status.pendding)
    slug = models.SlugField(max_length=255, verbose_name="slug", help_text=_("Majburyat tug'ulmasa tegmang"))
    post_viewed_count = models.IntegerField(default=0, verbose_name=_("Ko'rilganlik soni"), help_text=_("Tegilmasin !"))
    author_post = models.CharField(verbose_name=_("Yangilik yoki E'lon muallifi"), max_length=300, default="TKTI axborot xizmati")
    added_at = models.DateTimeField(verbose_name=_("Vaqt & sana"))
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="update_news_user")
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "news"
        managed = True
        verbose_name = _("Yangiliklar va E'lonlar")
        verbose_name_plural = _("Yangiliklar va E'lonlar")


    def __str__(self):
        return str(self.title) if self.title else None




