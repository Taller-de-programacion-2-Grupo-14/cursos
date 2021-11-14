from fastapi import Query
from typing import Optional, List

MAX_PRICE = 10000000
MIN_PRICE = 0


class CourseQueryParams:
    def __init__(
        self,
        name: Optional[str] = Query(None, min_length=1, max_length=255),
        creator_name: Optional[List[str]] = Query(None, min_length=1, max_length=50),
        hashtags: Optional[List[str]] = None,
        type: Optional[List[str]] = None,
        exams: Optional[int] = Query(None, ge=0),
        subscription: Optional[List[str]] = None,
        location: Optional[str] = Query(None, min_length=3, max_length=255),
        amount_students: Optional[int] = Query(None, ge=0),
        min_price: Optional[int] = Query(None, ge=MIN_PRICE),
        max_price: Optional[int] = Query(None, le=MAX_PRICE),
        offset: Optional[int] = Query(None, ge=0),
        limit: Optional[int] = Query(None, ge=500),
    ):
        self.name = name
        self.creatorName = creator_name
        self.hashtags = hashtags
        self.type = type
        self.exams = exams
        self.subscription = subscription
        self.location = location
        self.amountStudents = amount_students
        self.minPrice, self.maxPrice = self._getCorrectPrice(min_price, max_price)
        self.offset = offset
        self.limit = limit

    def _getCorrectPrice(self, minPrice, maxPrice):
        if minPrice is None and maxPrice is None:
            return None, None
        if minPrice is not None and maxPrice is None:
            return minPrice, MAX_PRICE
        if minPrice is None and maxPrice is not None:
            return MIN_PRICE, maxPrice
        return minPrice, maxPrice


class UsersQueryParams:
    def __init__(
        self,
        first_names: Optional[List[str]] = Query(None, min_length=1, max_length=255),
        last_names: Optional[List[str]] = Query(None, min_length=1, max_length=255),
        locations: Optional[List[str]] = Query(None, min_length=3, max_length=255),
        interests: Optional[List[str]] = None,
    ):
        self.firstName = first_names
        self.lastName = last_names
        self.location = locations
        self.interest = interests
