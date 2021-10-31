from pydantic import BaseModel, Field


class CreateCourseSchema(BaseModel):
    course_name: str = Field(min_length=1, max_length=255)
    course_description: str
    hashtags: str
    course_type: str
    amount_exams: int = Field(ge=0)
    subscription: str
    location: str = Field(min_length=3, max_length=255)
    user_id: int
