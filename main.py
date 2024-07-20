from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine, Base, get_db
from typing import Optional
from auth import pwd_context
from auth import authenticate_user,  create_access_token, get_current_user
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"Welcome"}

@app.post("/signup/", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    check_mail = crud.get_user_by_email(db, email=user.email)
    if check_mail:
        raise HTTPException(status_code=400, detail="Email already registered")
    check_username = crud.get_user_by_username(db, username=user.username)
    if check_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    new_user = crud.create_user(db=db,user=user,hashed_password=hashed_password)
    return {"Message": "Registration Successful", "data":new_user}

@app.post("/login/")

def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
#get user from database by email
@app.get('/user/')
def get_user(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email (db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Successfull", "data": user}

@app.post("/add_course/")
def add_course (payload: schemas.CourseCreate, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_course = crud.create_course(db=db, course=payload, user_id=user.id)
    return {"Message": "Course added successfully", "data": new_course}

# to get courses created by the user
@app.get("/courses/")
def get_courses(db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    courses = crud.get_courses (db=db, user_id=user.id)
    return {"message": "Successfull", "data": courses}

#get all courses without authorization
@app.get('/all_courses/')
def get_all_courses(db: Session = Depends(get_db)):
    course = crud.get_all_courses(db)
    return {"message": "Successfull", "data": course}


#get courses created by user from database by ID
@app.get('/course/')
def get_course(course_id:int, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user) ):
    course = crud.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to view this course")
    return {"message": "Successfull", "data": course}

@app.put("/courses/{course_id}")
def update_course(course_id: int, payload: schemas.CourseUpdate, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    course = crud.get_course_by_id(db=db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.user_id!= user.id:
         raise HTTPException(status_code=403, detail="You are not authorized to update this course")
    crud.update_course(db, course_id, payload)
    return {"message": "Course updated successfully", "data": course}

@app.delete("/course/{course_id}")

def delete_course(course_id: int, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    course = crud.get_course_by_id(db=db, course_id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this course")
    crud.delete_course(db, course_id)
    return {"message": "Course deleted successfully"}