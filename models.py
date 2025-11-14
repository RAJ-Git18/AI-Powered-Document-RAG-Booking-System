from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import date, time
import uuid


class BookingModel(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: str= Field(max_length=100)
    email: EmailStr
    date: date
    time: time
