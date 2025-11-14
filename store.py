from database import engine
from sqlmodel import Session
from models import BookingModel
from datetime import date, time


def storeBookingInfo(booking_dict: dict):
    try:
        booking_date = date.fromisoformat(booking_dict["date"])
        booking_time = time.fromisoformat(booking_dict["time"])

        booking = BookingModel(
            name=booking_dict["name"],
            email=booking_dict["email"],
            date=booking_date,
            time=booking_time,
        )

        with Session(engine) as session:
            session.add(booking)
            session.commit()
            session.refresh(booking)

        return {"message": "Booking stored successfully", "booking_id": str(booking.id)}

    except Exception as e:
        raise ValueError(f"Unable to store booking: {e}")
