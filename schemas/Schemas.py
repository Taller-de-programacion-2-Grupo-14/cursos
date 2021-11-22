from pydantic import BaseModel, Field, validator
from exceptions.CourseException import InvalidSubscriptionType
SUBSCRIPTION_TYPES = ["basico", "estandar", "premium"]


class CreateCourseSchema(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str
    hashtags: str
    type: str
    exams: int = Field(ge=0)
    subscription: str
    location: str = Field(min_length=3, max_length=255)
    user_id: int

    @validator("subscription")
    def validSubscriptionType(cls, subscription):
        if subscription.lower() not in SUBSCRIPTION_TYPES:
            raise InvalidSubscriptionType(SUBSCRIPTION_TYPES)
        return subscription.lower()


class DeleteCourseSchema(BaseModel):
    id: int
    user_id: int


class EditCourseInfoSchema(BaseModel):
    user_id: int
    name: str = Field(min_length=1, max_length=255)
    description: str
    location: str = Field(min_length=3, max_length=255)
    hashtags: str


class CollaboratorSchema(BaseModel):
    user_id: int
    id: int


class RemoveCollaboratorSchema(BaseModel):
    user_id: int
    user_to_remove: int
    id: int


class UserSchema(BaseModel):
    user_id: int
