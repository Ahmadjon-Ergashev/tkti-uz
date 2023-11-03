from rest_framework import viewsets, mixins
from drf_yasg.utils import swagger_auto_schema

from main.models import posts, widgets
from api.posts import query_params, serializers



class StudyProgramView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = posts.StudyProgram.objects.all().order_by("-added_at")
    serializer_class = serializers.StudyProgramSerializer

    def get_queryset(self):
        queryset = super().get_queryset().none()
        year = self.request.query_params.get("year")
        faculty = self.request.query_params.get("faculty")
        study_way = self.request.query_params.get("study_way")
        department = self.request.query_params.get("department")
        if year and faculty and department and study_way:
            queryset = super().get_queryset().filter(year=year, faculty=faculty, department=department, study_way=study_way)
        return queryset
    
    @swagger_auto_schema(manual_parameters=query_params.study_program_query())
    def list(self, request, *args, **kwargs):
        return super(StudyProgramView, self).list(request, *args, **kwargs)
    

class FacultyView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ get all faculties list """
    queryset = posts.Posts.objects.all()
    serializer_class = serializers.PostsSerializers

    def get_queryset(self):
        queryset = super().get_queryset().filter(status=widgets.Status.published, faculty=True)
        return queryset
    


class DepartmentsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = posts.Departments.objects.all()
    serializer_class = serializers.DepartmentsSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        faculty = self.request.query_params.get("faculty")
        if faculty:
            queryset = queryset.filter(faculty=faculty).order_by("-added_at")
        else:
            queryset = queryset.none()
        return queryset
    
    @swagger_auto_schema(manual_parameters=query_params.department_query())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class AdmistrationsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = posts.UniversityAdmistrations.objects.all().order_by("order_num")
    serializer_class = serializers.AdmistationSerializer


class TalentedStudentsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = posts.TalentedStudents.objects.all().order_by("-added_at")
    serializer_class = serializers.TalentedStudentsSerializers

    
    
