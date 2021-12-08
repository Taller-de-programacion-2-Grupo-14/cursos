from fastapi import Query
from typing import Optional
from exceptions.CourseException import InvalidStatusType

STATUS = {"aprobado": "approved", "desaprobado": "failed", "en curso": "on course"}


def getFilters(filtersDic):
    filters = {}
    for filterName, value in filtersDic.items():
        if value is not None:
            filters[filterName] = value.lower() if type(value) == str else value
    return filters


class CourseQueryParams:
    def __init__(
        self,
        name: Optional[str] = Query(None, min_length=1, max_length=255),
        creator_first_name: Optional[str] = Query(None, min_length=3, max_length=50),
        creator_last_name: Optional[str] = Query(None, min_length=3, max_length=50),
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
            "creator_first_name": creator_first_name,
            "creator_last_name": creator_last_name,
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


class HistoricalQueryParams:
    def __init__(
        self,
        status: Optional[str] = Query(None),
        offset: Optional[int] = Query(0, ge=0),
        limit: Optional[int] = Query(500, le=500),
    ):
        if status is not None:
            if status.lower() not in STATUS:
                raise InvalidStatusType(STATUS.keys())
            else:
                status = STATUS[status.lower()]
        self.filters = {
            "status": status,
            "offset": offset,
            "limit": limit,
        }

    def getFilters(self):
        return getFilters(self.filters)
