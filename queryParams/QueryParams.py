from fastapi import Query
from typing import Optional


def getFilters(filtersDic, offset, limit):
    filters = {}
    for filterName, value in filtersDic.items():
        if value is not None:
            filters[filterName] = value
    return {
        "filters": filters if len(filters) else None,
        "offset": offset,
        "limit": limit,
    }


class CourseQueryParams:
    def __init__(
        self,
        name: Optional[str] = Query(None, max_length=255),
        creator_name: Optional[str] = Query(None, max_length=50),
        hashtags: Optional[str] = None,
        course_type: Optional[str] = None,
        exams: Optional[int] = Query(None, ge=0),
        subscription: Optional[str] = None,
        location: Optional[str] = Query(None, max_length=255),
        free_text: Optional[str] = Query(None, max_length=255),
        offset: Optional[int] = Query(0, ge=0),
        limit: Optional[int] = Query(100, le=500),
    ):
        self.filters = {
            "name": name,
            "creatorName": creator_name,
            "hashtags": hashtags,
            "type": course_type,
            "exams": exams,
            "subscription": subscription,
            "location": location,
            "freeText": free_text,
        }
        self.offset = offset
        self.limit = limit

    def getFilters(self):
        return getFilters(self.filters, self.offset, self.limit)


class UsersQueryParams:
    def __init__(
        self,
        first_name: Optional[str] = Query(None, max_length=255),
        last_name: Optional[str] = Query(None, max_length=255),
        subscribers: Optional[bool] = Query(True),
        offset: Optional[int] = Query(0, ge=0),
        limit: Optional[int] = Query(100, le=500),
    ):
        self.filters = {
            "firstName": first_name,
            "lastName": last_name,
            "subscribers": subscribers,
        }
        self.offset = offset
        self.limit = limit

    def getFilters(self):
        return getFilters(self.filters, self.offset, self.limit)
