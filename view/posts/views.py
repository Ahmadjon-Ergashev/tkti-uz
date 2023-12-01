from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404

# local models
from main.models import (
    posts, news, widgets
)


def Home(request):
    """ for home page view """
    about_us = {
        "about_us": _("Biz xaqimizda"),
        "section_1": _("""
            Toshkent kimyo-texnologiya instituti (TKTI, http://tkti.uz) - kimyoviy texnologiya (organik va noorganik moddalar, 
            polimerlar, silikat va qiyin eruvchan materiallar, nodir va kamyob metallar kimyoviy texnologiyasi), oziq-ovqat texnologiyasi, 
            neft va gazni qayta ishlash, ekologiya, biotexnologiya, enologiya, sellyuloza va yogʻochga ishlov berish texnologiyasi va b. yo‘nalishlar 
            boyicha yuqori malakali mutaxassislar tayyorlashga ixtisoslashgan Markaziy Osiyodagi yetakchi universitetlardan biri hisoblanadi.
        """),
        "section_2": _("""
            Toshkent kimyo-texnologiya instituti 1991-yil 6-maydagi O‘zbekiston Respublikasi Prezidentining Farmoni bilan tashkil etilgan. 
            TKTI respublikada oliy texnik ta’lim darajasini oshirish, 
            muhandislik va ilmiy kadrlar tayyorlashni takomillashtirish maqsadida 1929 yildan beri faoliyat yuritayotgan sobiq Toshkent politexnika institutining bir necha fakultetlari negizida tashkil etilgan. 
            Institut o‘z faoliyati davomida mamlakatimiz kimyo, neft-gaz, oziq-ovqat, qurilish sanoati va iqtisodiyotining boshqa tarmoqlari uchun 10 mingdan ortiq yuqori malakali muhandis-texnologlar tayyorladi.
        """),
        "section_3": _("""
            Toshkent kimyo-texnologiya instituti Oʻzbekistondagi yetakchi kimyo-texnologiya oliy oʻquv yurtiboʻlib, oʻquv, ilmiy-tadqiqot, 
            pedagogik va tarbiyaviy faoliyatni amalga oshiradi. Institut tuzilmasiga Toshkent shahridagi Bosh kampus, Shahrisabz va Yangiyerdagi filiallar kiradi.
            Toshkent shahridagi Bosh kampusda 5 ta fakultet, 24 ta kafedra, 6 ta ishlab chiqarish oʻquv markazlari va 12 ta ilmiylaboratoriyalar mavjud.
        """)
    }
    translate_words = {
        "arxiv": _("Arxiv"),
        "all": _("Barchasi"),
        "search": _("Qidirish"),
        "events": _("Voqealar"),
        "title": _("Bosh sahifa"),
        "faculty_title": _("Fakultetlar"),
        "ads_section_title": _("E'lonlar"),
        "sp_way": _("Yo'nalishni tanlang"),
        "sp_type": _("Ta'lim turini tanlang"),
        "sp_faculty": _("Fakultetni tanlang"),
        "videos_section_title": _("Videolar"),
        "the_most_read": _("Top yangiliklar"),
        "upcoming": _("Yaqinlashib kelayotganlar"),
        "nth_faculty": _("tarkibidagi kafedralar"),
        "usuful_links_title": _("Foydali havolalar"),
        "the_last_news": _("Eng so'ngi yangiliklar"),
        "study_way_title": _("Ta'lim dasturi katalogi"),
        "talented_student_title": _("Iqtidorli talabalar"),
        "not_found_404": _("Afsuski hechqanday ma'lumot topilmadi :("),
    }
    objects_list = {
        "header_img": widgets.HeaderIMG.objects.all().order_by("order_num"),
        "statistika": widgets.Statistika.objects.all().order_by("-added_at"),
        "usefull_links": widgets.UsefullLinks.objects.all().order_by("-add_time"),
        "talented_students": posts.TalentedStudents.objects.order_by("-added_at").all(),
        "the_photos_home": widgets.PhotoGallary.objects.order_by("-added_at")[:6].all(),
        "all_events": news.Events.objects.filter(status="pub").order_by("added_at")[:8].all(),
        "the_last_ads_4": news.Ads.objects.filter(status="pub").order_by("-added_at")[:4].all(),
        "the_last_ads_8": news.Ads.objects.filter(status="pub").order_by("-added_at")[4:12].all(),
        "the_last_news_4": news.News.objects.filter(status="pub").order_by("-added_at")[:4].all(),
        "the_last_news_8": news.News.objects.filter(status="pub").order_by("-added_at")[4:12].all(),
        "the_last_videos": news.VideoGallery.objects.filter(status="pub").order_by("-added_at")[:6].all(),
        "the_most_view_news_4": news.News.objects.filter(status="pub").order_by("-post_viewed_count")[:4].all(),
        "the_most_view_news_8": news.News.objects.filter(status="pub").order_by("-post_viewed_count")[4:12].all(),
        "arxiv_events": news.Events.objects.filter(status="pub", added_at__lte=timezone.now()).order_by("added_at")[:8].all(),
        "upcoming_events": news.Events.objects.filter(status="pub", added_at__gte=timezone.now()).order_by("added_at")[:8].all(),
    }
    context = translate_words | objects_list | about_us 
    return render(request, "home.html", context)



class PostsListView(ListView):
    """ get all posts what connected to navbar """
    model = posts.Posts
    paginate_by = 5
    ordering = ["-added_at"]
    template_name = "pages/posts/posts.html"

    def get_queryset(self):
        navbar_slug = self.kwargs["navbar_slug"]
        if navbar_slug == "boglanish":
            qs = posts.ContactSection.objects.all().order_by("order_num")
        elif navbar_slug == "bolim-va-markazlar":
            qs = posts.SectionsAndCenters.objects.all().order_by("-added_at")
        elif navbar_slug == "institut-rahbariyati":
            qs = posts.UniversityAdmistrations.objects.all().order_by("order_num")
        elif navbar_slug == "iqtidorli-talabalar":
            qs = posts.TalentedStudents.objects.all().order_by("-added_at")
        else:
            qs = super().get_queryset().filter(status=widgets.Status.published, navbar__slug=navbar_slug).order_by("-added_at")

        one_obj = posts.Posts.objects.filter(navbar__slug=navbar_slug)
        if len(one_obj) == 1:
            one_obj = one_obj.first()
            one_obj.post_viewed_count += 1
            one_obj.save()
        return qs 
    
    def get_context_data(self, **kwargs):
        navbar_name = posts.Navbar.objects.get(slug=self.kwargs["navbar_slug"])
        context = super().get_context_data(**kwargs)
        context["title"] = navbar_name.name
        context["parent"] = navbar_name.parent
        context["title_slug"] = navbar_name.slug
        try:
            context["category_list"] = posts.Navbar.objects.filter(parent_id=navbar_name.parent.id)
        except AttributeError:
            context["category_list"] = navbar_name.get_children()
        try:
            context["pdf_file"] = context["object_list"][0].pdf_file
        except Exception:
            context["pdf_file"] = ""
        context["home"] = _("Bosh sahifa")
        context["empty"] = _("Afsuski hozircha ma'lumotlar topilmadi :(")
        return context


class PostDetailView(DetailView):
    """ get detail of posts """
    model = posts.Posts
    template_name = "pages/posts/post_detail.html"

    def get_object(self, queryset=None):
        post_slug = self.kwargs["post_slug"]
        obj = get_object_or_404(posts.Posts, slug=post_slug)
        obj.post_viewed_count += 1
        obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context["object"]
        navbar = posts.Navbar.objects.get(slug=post.navbar.slug)
        context["title"] = navbar.name
        context["depended_news"] = _("Mavzuga aloqador yangiliklar") 
        # error bor
        context["faculty_title"] = _("Fakultet ma'muryati")
        context["departments_title"] = _("Fakultet kafedralari")
        context["parent"] = navbar.parent.name
        try:
            context["category_list"] = posts.Navbar.objects.filter(parent_id=navbar.parent.id)
            context["pdf_file"] = post.pdf_file.url
        except AttributeError:
            context["category_list"] = navbar.get_children()
        except ValueError:
            context["pdf_file"] = ""
        return context


class DepartmentsDetailView(DetailView):
    """ departments detail view """
    model = posts.Departments
    template_name = "pages/posts/departments_detail.html"

    def get_object(self, queryset=None):
        dept_slug = self.kwargs['dept_slug']
        obj = get_object_or_404(posts.Departments, slug=dept_slug)
        obj.post_viewed_count += 1
        obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context["object"]
        context["departments_list"] = posts.Departments.objects.all().order_by("name")
        context["title"] = obj.name
        context["title_bar"] = _("Kafedralar")     
        return context


class SectionsDetailView(DetailView):
    """ bo'lim va markazlar """
    model = posts.SectionsAndCenters
    template_name = "pages/posts/sections_detail.html"

    def get_object(self, queryset=None):
        post_slug = self.kwargs["post_slug"]
        obj = get_object_or_404(posts.SectionsAndCenters, slug=post_slug)
        return obj
    

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        obj = data["object"]
        navbar = posts.Navbar.objects.get(slug=obj.navbar.slug)
        data["title"] = obj.title
        data["title"] = navbar.name
        data["parent"] = navbar.parent.name
        try:
            data["category_list"] = posts.Navbar.objects.filter(parent_id=navbar.parent.id)
        except AttributeError:
            data["category_list"] = navbar.get_children()    
        return data
    

class LearningWayDetailView(DetailView):
    model = posts.LearningWay
    template_name = "pages/study_way/study_way_list.html"

    def get_object(self, queryset=None):
        id = self.kwargs["id"]
        obj = get_object_or_404(posts.LearningWay, id=id)
        edu_areas = posts.EducationalAreas.objects.filter(study_way=obj.id)
        if len(edu_areas) == 1:
            edu_area = edu_areas.first()
            edu_area.post_viewed_count += 1
            edu_area.save()
        return obj
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        obj = data["object"]
        edu_areas = posts.EducationalAreas.objects.filter(study_way=obj.id)
        if len(edu_areas) == 1:
            semesters = widgets.Semesters.objects.all()
            modules_by_semester = {semester: posts.ModuleOfStudyPrograme.objects.filter(educational_area=edu_areas.first().id, semester=semester) for semester in semesters}
            data["modules_by_semester"] = modules_by_semester
        data["title"] = obj.name
        data["name"] = _("Nomi")
        data["view"] = _("Ko'rish")
        data["desc"] = _("Ta'lim dasturi xaqida")
        data["requarements"] = _("Kirish talablari")
        data["full_time_fee_title"] = _("Kundizgi ta'lim uchun")
        data["full_time_night_fee_title"] = _("Kechgi ta'lim uchun")
        data["you_may_become"] = _("Qachonki o'qishni bitirganingizda")
        data["full_time_external_fee_title"] = _("Sirtqi ta'lim uchun")
        data["modul_title"] = _("Semestrlar bo'yicha o'quv dasturi moduli")
        data["educational_areas"] = posts.EducationalAreas.objects.filter(study_way=obj.id)
        return data


class EducationalAreaView(ListView):
    model = posts.EducationalAreas
    template_name = "pages/study_way/study_way_list.html"

    def get_queryset(self):
        study_way = self.kwargs["study_way"]
        queryset = super().get_queryset().filter(study_way=study_way)
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if len(data["object_list"]) == 1:
            obj = data["object_list"][0]
            semesters = widgets.Semesters.objects.all()
            modules_by_semester = {semester: posts.ModuleOfStudyPrograme.objects.filter(educational_area=obj.id, semester=semester) for semester in semesters}
            data["modules_by_semester"] = modules_by_semester

        data["name"] = _("Nomi")
        data["view"] = _("Ko'rish")
        data["desc"] = _("Ta'lim dasturi xaqida")
        data["title"] = data["object_list"][0].name 
        data["requarements"] = _("Kirish talablari")
        data["full_time_fee_title"] = _("Kundizgi ta'lim uchun")
        data["full_time_night_fee_title"] = _("Kechgi ta'lim uchun")
        data["you_may_become"] = _("Qachonki o'qishni bitirganingizda")
        data["full_time_external_fee_title"] = _("Sirtqi ta'lim uchun")
        data["modul_title"] = _("Semestrlar bo'yicha o'quv dasturi moduli")
        return data
    

class EducationalAreaDetailView(DetailView):
    model = posts.EducationalAreas
    template_name = "pages/study_way/study_way_detail.html"

    def get_object(self, queryset=None):
        id = self.kwargs["id"]
        obj = get_object_or_404(posts.EducationalAreas, id=id)
        obj.post_viewed_count += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        obj = data["object"]
        semesters = widgets.Semesters.objects.all()
        modules_by_semester = {semester: posts.ModuleOfStudyPrograme.objects.filter(educational_area=obj.id, semester=semester) for semester in semesters}
        data["name"] = _("Nomi")
        data["title"] = obj.name
        data["view"] = _("Ko'rish")
        data["parent"] = obj.study_way
        data["desc"] = _("Ta'lim dasturi xaqida")
        data["requarements"] = _("Kirish talablari")
        data["modules_by_semester"] = modules_by_semester
        data["full_time_fee_title"] = _("Kundizgi ta'lim uchun")
        data["full_time_night_fee_title"] = _("Kechgi ta'lim uchun")
        data["you_may_become"] = _("Qachonki o'qishni bitirganingizda")
        data["full_time_external_fee_title"] = _("Sirtqi ta'lim uchun")
        data["modul_title"] = _("Semestrlar bo'yicha o'quv dasturi moduli")
        return data
    