from drf_yasg import openapi

def study_program_query():
    parameters = [
        openapi.Parameter("year", openapi.IN_QUERY, description="Yilni tanlang", type=openapi.TYPE_INTEGER),
        openapi.Parameter("faculty", openapi.IN_QUERY, description="Fakultetni tanlang", type=openapi.TYPE_STRING),
        openapi.Parameter("department", openapi.IN_QUERY, description="Kafedrani tanlang", type=openapi.TYPE_STRING),
        openapi.Parameter("study_way", openapi.IN_QUERY, description="Ta'lim darajase", enum=["high", "higher"], type=openapi.TYPE_STRING)
    ]
    return parameters



def department_query():
    faculty = openapi.Parameter("faculty", openapi.IN_QUERY, description="facultet idsi", type=openapi.TYPE_STRING)
    return [faculty]


def learning_way_query():
    study_degree = openapi.Parameter("study_degree", openapi.IN_QUERY, description="Ta'lim darajasi idsi", type=openapi.TYPE_STRING)
    faculty = openapi.Parameter("faculty", openapi.IN_QUERY, description="facultet idsi", type=openapi.TYPE_STRING)
    return [study_degree, faculty]