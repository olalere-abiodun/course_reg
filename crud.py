from sqlalchemy.orm import Session
import models
import schemas

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(
        full_name = user.full_name,
        username = user.username,
        email = user.email,
        level = user.level, 
        hashed_password = hashed_password
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username:str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_course(db: Session, course:schemas.CourseCreate, user_id: int = None):
    db_course = models.Courses(
        course_name = course.course_name,
        course_title = course.course_title,
        lecturer = course.lecturer,
        user_id = user_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

# Get all courses
def get_all_courses(db: Session):
    return db.query(models.Courses).all()

# Get courses created by a user
def get_courses(db: Session, user_id: int):
    return db.query(models.Courses).filter(models.Courses.user_id == user_id).all()

def get_course_by_id(db: Session, course_id: int):
    return db.query(models.Courses).filter(models.Courses.id == course_id).first()

def update_course(db: Session, course_id: int, new_course: schemas.CourseUpdate):
    course = get_course_by_id(db, course_id)
    if not course: 
        return {"detail": "No course with the id " + str(course_id)}
    course.course_name = new_course.course_name
    course.course_title = new_course.course_title
    course.lecturer = new_course.lecturer
    db.add(course)
    db.commit()
    db.refresh(course)
    return {"message":"Course updated successfully", "data": course}

def delete_course(db:Session, course_id: int):
    course = get_course_by_id(db, course_id)
    if not course:
        return {"detail": "No course with the id " + str(course_id)}
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}

