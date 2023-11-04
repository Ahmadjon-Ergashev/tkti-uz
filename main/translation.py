from modeltranslation.translator import register, TranslationOptions


from main.models import posts, news, widgets

""" posts models translations file """

@register(posts.Navbar)
class NavbarTranslation(TranslationOptions):
    fields = ("name", )


@register(posts.Posts)
class PostsTranslation(TranslationOptions):
    fields = ("title", "subtitle", "post")


@register(posts.FacultyAdministration)
class FacultyAdministrationTranslation(TranslationOptions):
    fields = ("f_name", "job_name", "admission_day")


@register(posts.Departments)
class DepartmentsTranslation(TranslationOptions):
    fields = ("name", "post")


@register(posts.StudyProgram)
class StudyProgramTranslation(TranslationOptions):
    fields = ("title", )


@register(posts.ContactSection)
class ContactSectionTranslation(TranslationOptions):
    fields = ("title", "address")


@register(posts.Workers)
class WorkersTranslation(TranslationOptions):
    fields = ("f_name", )


@register(posts.SectionsAndCenters)
class SectionsAndCentersTranslation(TranslationOptions):
    fields = ("title", "about", "target", "activity")
    

@register(posts.UniversityAdmistrations)
class UniversityAdmistrationsTranslation(TranslationOptions):
    fields = ("f_name", "position", "admission_days", "short_info", 
              "scientific_direction", "main_tasks_in_position", "scientific_activity")
    

@register(posts.TalentedStudents)
class TalentedStudentsTranslation(TranslationOptions):
    fields = ("f_name", "desc")
    

@register(posts.BossSection)
class BossSectionTranslation(TranslationOptions):
    fields = ("f_name", )

""" news models translations file """
    

@register(news.Category)
class CategoryTranslation(TranslationOptions):
    fields = ("name", )
    

@register(news.News)
class NewsTranslation(TranslationOptions):
    fields = ("title", "subtitle", "post")
    

@register(news.Ads)
class AdsTranslation(TranslationOptions):
    fields = ("title", "subtitle", "post")
    

@register(news.VideoGallery)
class VideoGalleryTranslation(TranslationOptions):
    fields = ("title", )


""" widgets models translations file """
    
@register(widgets.Hashtag)
class HashtagTranslation(TranslationOptions):
    fields = ("name", )


@register(widgets.SocialNetworks)
class SocialNetworksTranslation(TranslationOptions):
    fields = ("name", )


@register(widgets.UsefullLinks)
class UsefullLinksTranslation(TranslationOptions):
    fields = ("name", )


@register(widgets.QuickLinks)
class QuickLinksTranslation(TranslationOptions):
    fields = ("name", )


@register(widgets.Statistika)
class StatistikaTranslation(TranslationOptions):
    fields = ("name", )


@register(widgets.Flag)
class FlagTranslation(TranslationOptions):
    fields = ("title", "description")


@register(widgets.CoatofArms)
class CoatofArmsTranslation(TranslationOptions):
    fields = ("title", "description")


@register(widgets.Anthem)
class AnthemTranslation(TranslationOptions):
    fields = ("title", "description")


@register(widgets.FaqCategory)
class FaqCategoryTranslation(TranslationOptions):
    fields = ("name", )


@register(widgets.Faq)
class FaqTranslation(TranslationOptions):
    fields = ("title", "answer")