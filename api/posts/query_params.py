from drf_yasg import openapi

def study_program_query():
    year = openapi.Parameter("year", openapi.IN_QUERY, description="Yilni tanlang", type=openapi.TYPE_INTEGER)
    faculty = openapi.Parameter("faculty__name", openapi.IN_QUERY, description="Fakultetni tanlang", type=openapi.TYPE_STRING)
    return [year, faculty]