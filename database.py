import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()  # load environment variables from.env.

SQLALCHEMY_DATABASE_URL = os.environ.get('DB_URL')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()