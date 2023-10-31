from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _


# local vars
from main.models import news, widgets


class NewsDetailView(DetailView):
    """ detail view for news and detail """
    model = news.News
    template_name = "pages/news_and_ada/detail.html"

    def get_object(self, queryset=None):
        slug = self.kwargs["obj_slug"]
        object = get_object_or_404(news.News, slug=slug)
        object.post_viewed_count += 1
        object.save()
        return object
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context["object"]
        context["title"] = _("Yangilik")
        try:
            domain = self.request.get_host()
            context["pdf_file"] = f"https://{domain}" + object.pdf_file.url
        except ValueError:
            context["pdf_file"] = ""
        return context


class AdsDetailView(DetailView):
    """ detail view for ads and detail """
    model = news.News
    template_name = "pages/news_and_ada/detail.html"

    def get_object(self, queryset=None):
        slug = self.kwargs["obj_slug"]
        object = get_object_or_404(news.Ads, slug=slug)
        object.post_viewed_count += 1
        object.save()
        return object
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context["object"]
        context["title"] = _("E'lon")
        try:
            domain = self.request.get_host()
            context["pdf_file"] = f"https://{domain}" + object.pdf_file.url
        except ValueError:
            context["pdf_file"] = ""
        return context
    

def Upload_Images(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = request.FILES.getlist('images') 
            for d in data:
                img = widgets.PhotoGallary.objects.create(image=d)
                img.save()
    return render(request, "widgets/upload_images.html") 