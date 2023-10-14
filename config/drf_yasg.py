# from rest_framework_swagger.views import get_swagger_view
from drf_yasg import openapi
from django.contrib import admin
from drf_yasg.views import get_schema_view


API_TITLE = 'TKTI.uz Doc'
API_DESCRIPTION = 'Toshkent Kimyo texnologiyalar universiteti rasmiy web sayti Doc'
yasg_schema_view = get_schema_view(
    openapi.Info(
        title=API_TITLE,
        default_version='v1',
        description=API_DESCRIPTION,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="turgunovzohidillo77@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

# schema_view = get_swagger_view(title=API_TITLE)


# admin.site.site_header = "Migrant Admin"
# admin.site.site_title = "Migrant Admin"
# admin.site.index_title = "Migrant Admin"