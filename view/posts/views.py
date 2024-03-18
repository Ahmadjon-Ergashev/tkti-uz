from django.views import View
from django.db.models import F
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404


# local models
from main.models import (
    posts, news, widgets
)


class Home(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        object_list_cache = cache.get('object_list_cache')
        if not object_list_cache:
            objects_list = {
                "header_img": widgets.HeaderIMG.objects.order_by("order_num").only("image"),
                "statistika": widgets.Statistika.objects.order_by("order_num").only(
                    "name", "icon", "url", "quantity"
                ),
                # "usefull_links": widgets.UsefullLinks.objects.order_by("-add_time").only(
                #     "name", "logo", "link"
                # ),
                "talented_students": posts.TalentedStudents.objects.order_by("-added_at").only(
                    "image", "f_name", "desc"
                ),
            }
            cache.set('object_list_cache', objects_list, 600)
            if object_list_cache is None:
                object_list_cache = {}
        context = object_list_cache
        return render(request, self.template_name, context)


class PostsListView(ListView):
    """ get all posts what connected to navbar """
    model = posts.Posts
    paginate_by = 5
    ordering = ["-added_at"]
    template_name = "pages/posts/posts.html"

    def get_queryset(self):
        navbar_slug = self.kwargs["navbar_slug"]
        if navbar_slug == "boglanish":
            qs = posts.ContactSection.objects.order_by("order_num").select_related("navbar")
        elif navbar_slug == "bolim-va-markazlar":
            qs = posts.SectionsAndCenters.objects.order_by("-added_at").select_related("navbar")
        elif navbar_slug == "institut-rahbariyati":
            qs = posts.UniversityAdmistrations.objects.order_by("order_num").select_related("navbar")
        elif navbar_slug == "iqtidorli-talabalar":
            qs = posts.TalentedStudents.objects.order_by("-added_at")
        else:
            qs = super().get_queryset().filter(
                status=widgets.Status.published, navbar__slug=navbar_slug
            ).order_by("-added_at").select_related("author", "update_user", "navbar")

        one_obj = posts.Posts.objects.filter(navbar__slug=navbar_slug)
        if len(one_obj) == 1:
            one_obj.update(post_viewed_count=F("post_viewed_count") + 1)
        return qs

    def get_paginate_by(self, queryset):
        navbar_slug = self.kwargs["navbar_slug"]
        if navbar_slug == "bolim-va-markazlar":
            return 32
        else:
            return self.paginate_by

    def get_context_data(self, **kwargs):
        navbar_name = posts.Navbar.objects.get(slug=self.kwargs["navbar_slug"])
        context = super().get_context_data(**kwargs)
        context["title"] = navbar_name.name
        context["parent"] = navbar_name.parent
        context["title_slug"] = navbar_name.slug
        if len(context["object_list"]) == 1:
            try:
                extra_pdf_list = widgets.ExtraFile.objects.filter(
                    post=context["object_list"][0]).only("name", "pdf_file")
                connected_faculty_dact = news.News.objects.filter(
                    faculty_dact=context["object_list"][0].id, status="pub").order_by("-added_at")[:12].only(
                    "title", "slug", "added_at", "post_viewed_count").prefetch_related(
                    "faculty_dact", "departments", "section_and_centers", "hashtag", "brm")

                context["extra_pdf_list"] = extra_pdf_list
                context["connected_faculty_dact"] = connected_faculty_dact
            except Exception as e:
                print(e, 141)
        try:
            context["category_list"] = posts.Navbar.objects.filter(parent_id=navbar_name.parent.id)
        except AttributeError:
            context["category_list"] = navbar_name.get_children()
        try:
            context["pdf_file"] = context["object_list"][0].pdf_file
        except Exception:
            context["pdf_file"] = ""
        context["connected_faqs"] = widgets.Faq.objects.filter(
            is_active=True, category=navbar_name.id).select_related("category")
        context["home"] = _("Bosh sahifa")
        context["depended_news"] = _("Mavzuga aloqador yangiliklar")
        context["depended_faq"] = _("Mavzuga aloqador savol va javoblar")
        context["empty"] = _("Afsuski hozircha ma'lumotlar topilmadi :(")
        context["brm"] = widgets.BRMItems.objects.all().order_by("number")
        context["digitizations"] = widgets.Digitization.objects.only("name", "icon")
        context["appeal"] = _("Rektorga murojaat")
        context["change_last_name"] = _("Familyani o'zgartirish")
        context["login_cabinet"] = _("Shaxsiy kabinetga kirish")
        context["lessons_schedule"] = _("Dars jadvali")
        context["students_hotel"] = _("Talabalar turar joyiga onlayn ariza berish")
        context["added_study"] = _("Toshkent kimyo-texnologiya instituti qo'shma talim dasturi")
        context["added_study_branch"] = _("Toshkent kimyo-texnologiya instituti qo'shma talim dasturi (Yangiyer filiali)")

        return context


class PostDetailView(DetailView):
    """ get detail of posts """
    model = posts.Posts
    template_name = "pages/posts/post_detail.html"

    def get_object(self, queryset=None):
        post_slug = self.kwargs["post_slug"]
        posts.Posts.objects.filter(slug=post_slug).update(post_viewed_count=F("post_viewed_count") + 1)
        obj = get_object_or_404(
            posts.Posts.objects.select_related("author", "update_user", "navbar"),
            slug=post_slug
        )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context["object"]
        try:
            extra_pdf_list = widgets.ExtraFile.objects.filter(
                post=post).only("name", "pdf_file")
            connected_faculty_dact = news.News.objects.filter(
                faculty_dact=post, status="pub").order_by("-added_at")[:12].only(
                "title", "slug", "added_at", "post_viewed_count").prefetch_related(
                "faculty_dact", "departments", "section_and_centers", "hashtag", "brm")
            context["extra_pdf_list"] = extra_pdf_list
            context["connected_faculty_dact"] = connected_faculty_dact
        except Exception as e:
            print(e, 141)
        navbar = posts.Navbar.objects.get(slug=post.navbar.slug)
        context["title"] = navbar.name
        context["depended_news"] = _("Mavzuga aloqador yangiliklar")
        context["bachelor_departments_way"] = posts.LearningWay.objects.filter(
            faculty=post, study_degree=1)
        context["master_departments_way"] = posts.LearningWay.objects.filter(
            faculty=post, study_degree=2
        )
        context["bachelor_departments_way_title"] = _("FAKULTETNING BAKALAVRIATURA YO‘NALISHLARI")
        context["master_departments_way_title"] = _("FAKULTETNING MAGISTRATURA YO‘NALISHLARI")
        context["faculty_title"] = _("Fakultet ma'muryati")
        context["departments_title"] = _("Fakultet kafedralari")
        context["parent"] = navbar.parent.name
        try:
            context["extra_pdf_list"] = widgets.ExtraFile.objects.filter(
                post=post).only("name", "pdf_file")
        except Exception as e:
            print(e)
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
        posts.Departments.objects.filter(slug=dept_slug).update(post_viewed_count=F("post_viewed_count") + 1)
        obj = get_object_or_404(posts.Departments, slug=dept_slug)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context["object"]
        try:
            context["conn_departments"] = news.News.objects.filter(
                departments=obj.id, status="pub").order_by("-added_at")[:12].only(
                        "title", "slug", "added_at", "post_viewed_count").prefetch_related(
                            "faculty_dact", "departments", "section_and_centers", "hashtag", "brm")
        except Exception as e:
            print(e, 141)
        context["depended_news"] = _("Mavzuga aloqador yangiliklar")
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
        try:
            data["conn_section_and_centers"] = news.News.objects.filter(
                section_and_centers=obj.id, status="pub").order_by("-added_at")[:12].only(
                    "title", "slug", "added_at", "post_viewed_count").prefetch_related(
                        "faculty_dact", "departments", "section_and_centers", "hashtag", "brm")
        except Exception as e:
            print(e, 141)
        navbar = posts.Navbar.objects.get(slug=obj.navbar.slug)
        data["title"] = obj.title
        data["title"] = navbar.name
        data["parent"] = navbar.parent.name
        data["about_section"] = _("Haqida")
        data["depended_news"] = _("Mavzuga aloqador yangiliklar")
        try:
            data["category_list"] = posts.Navbar.objects.filter(parent_id=navbar.parent.id)
        except AttributeError:
            data["category_list"] = navbar.get_children()
        return data


class LearningWayDetailView(DetailView):
    model = posts.LearningWay
    template_name = "pages/study_way/study_way_list.html"

    def get_object(self, queryset=None):
        obj_id = self.kwargs["id"]
        this_object = get_object_or_404(
            posts.LearningWay, id=obj_id
        )
        return this_object

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        obj = data["object"]
        education_areas = posts.EducationalAreas.objects.filter(
            study_way=obj.id).select_related(
                "study_way"
        )
        if len(education_areas) == 1:
            education_areas.update(post_viewed_count=F("post_viewed_count") + 1)

            # cache_key = f"modules_by_semester_{education_areas[0].id}"
            # cached_data = cache.get(cache_key)
            # if cached_data is not None:
            #     data["modules_by_semester"] = cached_data
            # else:
            #     grouped_data = {}
            #     for edu_area in education_areas:
            #         for module in edu_area.moduleofstudyprograme_set.select_related(
            #                 "semester", "educational_area"
            #         ):
            #             if module.semester in grouped_data:
            #                 grouped_data[module.semester].append(module)
            #             else:
            #                 grouped_data[module.semester] = [module]
            #
            #     # Cache the data with a specific timeout (e.g., 1 hour)
            #     cache.set(cache_key, grouped_data, 60 * 30)
            #
            #     data["modules_by_semester"] = grouped_data

            grouped_data = {}
            for edu_area in education_areas:
                for module in edu_area.moduleofstudyprograme_set.select_related(
                        "semester", "educational_area"
                ):
                    if module.semester in grouped_data:
                        grouped_data[module.semester].append(module)
                    else:
                        grouped_data[module.semester] = [module]

            # print(grouped_data.keys(), "*" * 150)
            # sorted_semesters = sorted(grouped_data.keys(), key=lambda x: x.name)
            #
            sorted_semesters = sorted((key for key in grouped_data.keys() if key is not None), key=lambda x: x.name)
            sorted_grouped_data = {semester: grouped_data[semester] for semester in sorted_semesters}
            # print(sorted_semesters)
            data["modules_by_semester"] = sorted_grouped_data

        data["title"] = obj.name
        data["name"] = _("Nomi")
        data["view"] = _("Ko'rish")

        data["desc"] = _("Sirtqi ta'lim dasturi haqida")
        data["desc_day"] = _("Kunduzgi ta'lim dasturi haqida")
        data["desc_evening"] = _("Kechki ta'lim dasturi haqida")

        data["requirements"] = _("Sirtqi ta'limga kirish talablari")
        data["requirements_day"] = _("Kundizgi ta'limga kirish talablari")
        data["requirements_evening"] = _("Kechki ta'limga kirish talablari")
        data["requirements_master"] = _("Magistraturaga kirish talablari")
        data["requirements_phd"] = _("PHD ga kirish talablari")
        data["requirements_dsc"] = _("DSC ga kirish talablari")

        data["dept_fee_title"] = _("Sirtqi ta'lim uchun 1 kredit miqdori")
        data["dept_fee_title_day"] = _("Kunduzgi ta'lim uchun 1 kredit miqdori")
        data["dept_fee_title_evening"] = _("Kechki ta'lim uchun 1 kredit miqdori")
        data["dept_fee_title_master"] = _("Magistratura yo'nalishi uchun 1 kredit miqdori")

        data["full_time_fee_title"] = _("Sirtqi ta'lim uchun 1 yillik kontrakt miqdori")
        data["full_time_fee_title_day"] = _("Kunduzgi ta'lim uchun 1 yillik kontrakt miqdori")
        data["full_time_fee_title_evening"] = _("Kechki ta'lim uchun 1 yillik kontrakt miqdori")
        data["full_time_fee_title_master"] = _("Magistratura yo'nalishi uchun 1 yillik kontrakt miqdori")

        data["theme_name"] = _("Mavzu Nomi")
        data["theme_teacher"] = _("Ilmiy rahbar")
        data["theme_finance"] = _("Moliyalashtirish")
        data["theme_download"] = _("Mavzular ro'yhatinni yuklab olish")

        data["you_may_become"] = _("Qachonki o'qishni bitirganingizda")
        data["modul_title"] = _("Semestrlar bo'yicha o'quv dasturi moduli")
        data["educational_areas"] = education_areas
        return data


class EducationalAreaView(ListView):
    model = posts.EducationalAreas
    template_name = "pages/study_way/study_way_list.html"

    def get_queryset(self):
        study_way = self.kwargs["study_way"]
        queryset = super().get_queryset().filter(study_way=study_way).select_related("study_way")
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        obj = data["object"]

        education_areas = posts.EducationalAreas.objects.filter(
            study_way=obj.id).select_related(
                "study_way"
        )
        if len(self.get_queryset()) == 1:
            education_areas.update(post_viewed_count=F("post_viewed_count") + 1)

        # cache_key = f"modules_by_semester_id_{education_areas[0].id}"

        # cached_data = cache.get(cache_key)
        # if cached_data is not None:
        #     data["modules_by_semester"] = cached_data
        # else:
            # grouped_data = {}
            # for edu_area in education_areas:
            #     for module in edu_area.moduleofstudyprograme_set.select_related(
            #             "semester", "educational_area"
            #     ):
            #         if module.semester in grouped_data:
            #             grouped_data[module.semester].append(module)
            #         else:
            #             grouped_data[module.semester] = [module]

            # cache.set(cache_key, grouped_data, 60 * 30)

            # data["modules_by_semester"] = grouped_data

        grouped_data = {}
        for edu_area in education_areas:
            for module in edu_area.moduleofstudyprograme_set.select_related(
                    "semester", "educational_area"
            ):
                if module.semester in grouped_data:
                    grouped_data[module.semester].append(module)
                else:
                    grouped_data[module.semester] = [module]

        sorted_semesters = sorted(grouped_data.keys(), key=lambda x: x.name)
        print(sorted_semesters, "*" * 150)

        sorted_grouped_data = {semester: grouped_data[semester] for semester in sorted_semesters}

        data["modules_by_semester"] = sorted_grouped_data

        data["name"] = _("Nomi")
        data["view"] = _("Ko'rish")
        data["desc"] = _("Ta'lim dasturi haqida")
        data["title"] = data["object_list"][0].name
        data["requirements"] = _("Kirish talablari")
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
        obj = posts.EducationalAreas.objects.filter(id=id).select_related("study_way")
        obj.update(post_viewed_count=F("post_viewed_count") + 1)
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        obj = data["object"]
        # education_areas = posts.EducationalAreas.objects.filter(
        #     study_way=obj.id).select_related(
        #     "study_way"
        # )
        # if len(education_areas) == 1:
        #     education_areas.update(post_viewed_count=F("post_viewed_count") + 1)

        grouped_data = {}
        for edu_area in obj:
            for module in edu_area.moduleofstudyprograme_set.select_related("semester", "educational_area"):
                if module.semester in grouped_data:
                    grouped_data[module.semester].append(module)
                else:
                    grouped_data[module.semester] = [module]
        data["modules_by_semester"] = grouped_data

        data["name"] = _("Nomi")
        data["title"] = obj.name
        data["view"] = _("Ko'rish")
        data["parent"] = obj.study_way
        data["desc"] = _("Ta'lim dasturi haqida")
        data["requirements"] = _("Kirish talablari")
        data["dept_fee_title"] = _("Kredit miqdori")
        data["full_time_fee_title"] = _("Kantrakt miqdori")
        data["you_may_become"] = _("Qachonki o'qishni bitirganingizda")
        data["modul_title"] = _("Semestrlar bo'yicha o'quv dasturi moduli")
        return data
