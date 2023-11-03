from drf_yasg import openapi


def faq_params():
    faq_category = openapi.Parameter("faq_category", openapi.IN_QUERY, description="faq category id", type=openapi.TYPE_STRING)
    return [faq_category]