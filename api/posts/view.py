from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView

from main.models import posts
from api.posts import query_params
from .serializers import (
    StudyProgramSerializer, PostsSerializers, DepartmentsSerializers
 )


class StudyProgramView(ListAPIView):
    queryset = posts.StudyProgram.objects.all().order_by("-added_at")
    serializer_class = StudyProgramSerializer

    def get_queryset(self):
        queryset = super().get_queryset().none()
        year = self.request.query_params.get("year")
        faculty = self.request.query_params.get("faculty")
        if year:
            queryset = queryset.filter(year=year)
        if faculty:
            queryset = queryset.filter(faculty__name__icontains=faculty)
        return queryset
    
    @swagger_auto_schema(manual_parameters=query_params.study_program_query())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class FacultyView(ListAPIView):
    queryset = posts.Posts.objects.all()
    serializer_class = PostsSerializers

    def get_queryset(self):
        queryset = super().get_queryset().filter(status=posts.Status.published, faculty=True)
        return queryset
    

class DepartmentsView(ListAPIView):
    queryset = posts.Departments.objects.all()
    serializer_class = DepartmentsSerializers

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