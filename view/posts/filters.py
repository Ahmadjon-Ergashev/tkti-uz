import django_filters

# local models
from main.models.posts import StudyProgram


class StudyWayFilters(django_filters.FilterSet):
    class Meta:
        model = StudyProgram
        fields = ["year", "faculty", "department", "study_way"]
    