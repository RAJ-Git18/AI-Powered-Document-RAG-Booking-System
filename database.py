from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

from models import BookingModel

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    if DATABASE_URL is not None:
        engine = create_engine(DATABASE_URL, echo=True)
except Exception as e:
    raise ValueError('App cannot be connected with database:-',e)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
