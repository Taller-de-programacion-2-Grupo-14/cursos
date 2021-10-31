from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError, validator
from models.Course import Course
from resources.Course import CourseController

class CourseCreateSchema(BaseModel):
    course_name: str
    course_description: str
    hashtags: str
    course_type: str
    amount_exams: int
    subscription: str
    location: str

    @validator('course_name')
    def name_must_have_len_greater_than_3(cls, v):
        if len(v) <= 3:
            raise ValueError('must be > 3')
        return v.title()


# ToDo:
# Crear diretorio validators y los importamos
# Crear todos los esquemas para los distintos tipos de post
# Cambiar nombre de los metodos
# Modificar como se devuelven los errores y las cosas en general
# Hacer tests

app = FastAPI()
courseService = Course({})
courseController = CourseController(courseService)


@app.post('/course/create')
def create_course(createData: CourseCreateSchema):
    return courseController.handle_course_create_post(createData.dict())

@app.get('/course/{course_id}')
def get_course(course_id: int):
    return courseController.handle_get_course(course_id)