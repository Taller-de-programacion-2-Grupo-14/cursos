from fastapi import Query
from typing import Optional


def getFilters(filtersDic):
    filters = {}
    for filterName, value in filtersDic.items():
        if value is not None:
            filters[filterName] = value
    return filters


class CourseQueryParams:
    def __init__(
        self,
        name: Optional[str] = Query(None, min_length=1, max_length=255),
        creator_name: Optional[str] = Query(None, min_length=3, max_length=50),
        hashtags: Optional[str] = Query(None, min_length=3, max_length=50),
        type: Optional[str] = None,
        exams: Optional[int] = Query(None, ge=0),
        subscription: Optional[str] = Query(
            None, regex="^([Bb]asico|[Ee]standar|[Pp]remium)$"
        ),
        location: Optional[str] = Query(None, min_length=3, max_length=255),
        free_text: Optional[str] = Query(None, max_length=255),
        offset: Optional[int] = Query(0, ge=0),
        limit: Optional[int] = Query(500, le=500),
    ):
        self.filters = {
            "name": name,
            "creatorName": creator_name,
            "hashtags": hashtags,
            "type": type,
            "exams": exams,
            "subscription": subscription,
            "location": location,
            "free_text": free_text,
            "offset": offset,
            "limit": limit,
        }

    def getFilters(self):
        return getFilters(self.filters)


class UsersQueryParams:
    def __init__(
        self,
        first_name: Optional[str] = Query(None, min_length=3, max_length=255),
        last_name: Optional[str] = Query(None, min_length=3, max_length=255),
        subscribers: Optional[bool] = Query(
            True,
            description="Type of user to search. True (default): subscribers, False: collaborators",
        ),
        offset: Optional[int] = Query(0, ge=0),
        limit: Optional[int] = Query(500, le=500),
    ):
        self.filters = {
            "first_name": first_name,
            "last_name": last_name,
            "subscribers": subscribers,
            "offset": offset,
            "limit": limit,
        }

    def getFilters(self):
        return getFilters(self.filters)
