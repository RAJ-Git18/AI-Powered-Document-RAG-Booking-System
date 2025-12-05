from .database import get_session
from models import BookingModel
from datetime import date, time
from sqlmodel import Session
from fastapi import Depends


def storeBookingInfo(booking_dict: dict, db: Session = Depends(get_session)):
    try:
        booking_date = date.fromisoformat(booking_dict["date"])
        booking_time = time.fromisoformat(booking_dict["time"])

        booking = BookingModel(
            name=booking_dict["name"],
            email=booking_dict["email"],
            date=booking_date,
            time=booking_time,
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return {"message": "Booking stored successfully", "booking_id": str(booking.id)}

    except Exception as e:
        raise ValueError(f"Unable to store booking: {e}")
