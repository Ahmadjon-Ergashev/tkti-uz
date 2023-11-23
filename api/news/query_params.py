from enum import Enum
from drf_yasg import openapi

class GetType(Enum):
    latest: str = "latest"
    most_read: str = "most_read"


def news_queries():
    get_type = openapi.Parameter('get_type', openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=[value.value for value in GetType], required=False)
    start = openapi.Parameter('start', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False)
    end = openapi.Parameter('end', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False)
    return [get_type, start, end]


class EventGetType(Enum):
    all: str = "all"
    past: str = "past"
    upcoming: str = "upcoming"


def events_queries():
    event_get_type = openapi.Parameter("get_type", openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False, enum=[i.value for i in EventGetType])
    start = openapi.Parameter('start', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=0, required=False)
    end = openapi.Parameter('end', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False)
    return [event_get_type, start, end]

