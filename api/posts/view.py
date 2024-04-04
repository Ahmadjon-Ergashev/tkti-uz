from rest_framework import viewsets, mixins
from drf_yasg.utils import swagger_auto_schema

from main.models import posts, widgets
from api.posts import query_params, serializers


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
    serializer_class = serializers.AdministrationSerializer


class TalentedStudentsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = posts.TalentedStudents.objects.all().order_by("-added_at")
    serializer_class = serializers.TalentedStudentsSerializers


class StudyDegreeView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = posts.StudyDegrees.objects.all()
    serializer_class = serializers.StudyDegreesSerialziers


class LearningWayView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = posts.LearningWay.objects.all().order_by("name")
    serializer_class = serializers.LearningWaySerializers
    
    def get_queryset(self):
        queryset = super().get_queryset()
        study_degree = self.request.query_params.get("study_degree")
        faculty = self.request.query_params.get("faculty")
        if faculty and study_degree:
            queryset = queryset.filter(study_degree=study_degree, fields_edu=faculty).order_by("-added_at")
        else:
            queryset = queryset.none()
        return queryset
    
    @swagger_auto_schema(manual_parameters=query_params.learning_way_query())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    
    
