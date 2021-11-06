from pydantic import BaseModel, Field, validator


class CreateCourseSchema(BaseModel):
    course_name: str = Field(min_length=1, max_length=255)
    course_description: str
    hashtags: str
    course_type: str
    amount_exams: int = Field(ge=0)
    subscription: str
    location: str = Field(min_length=3, max_length=255)
    user_id: int


class DeleteCourseSchema(BaseModel):
    course_id: int
    user_id: int


class EditCourseInfoSchema(BaseModel):
    course_id: int
    user_id: int
    course_name: str = Field(min_length=1, max_length=255)
    course_description: str
    amount_exams: int = Field(ge=0)
    location: str = Field(min_length=3, max_length=255)


class CollaboratorSchema(BaseModel):
    user_id: int
    user_to_remove: int = None
    course_id: int
