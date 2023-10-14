from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView

from main.models.posts import StudyProgram
from .query_params import study_program_query
from .serializers import StudyProgramSerializer


class StudyProgramView(ListAPIView):
    queryset = StudyProgram.objects.all().order_by("-added_at")
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
    
    @swagger_auto_schema(manual_parameters=study_program_query())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)