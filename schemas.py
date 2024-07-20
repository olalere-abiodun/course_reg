from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    
class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    full_name: str
    email: str
    level: int
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: str
    level: int
    password: str
    
class CourseBase(BaseModel):
    course_name: str
    course_title: str
    lecturer: str

class Course(CourseBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_orm=True)

class CourseCreate(BaseModel):
    course_name: str
    course_title: str
    lecturer: str

class CreateCourse(CourseCreate):
    pass

class CourseUpdate(BaseModel):
    course_name: str
    course_title: str
    lecturer: str
