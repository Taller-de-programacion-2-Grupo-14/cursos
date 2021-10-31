from pydantic import BaseModel, Field


class EditCourseInfoSchema:
    course_id: int
    user_id: int
    course_name: str = Field(min_length=1, max_length=255)
    course_description: str
    amount_exams: int = Field(ge=0)
    location: str = Field(min_length=3, max_length=255)