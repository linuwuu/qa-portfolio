from typing import Optional

from pydantic import BaseModel, StrictBool, StrictInt, StrictStr


# strict: без них pydantic молча превращает "5" в 5, и проверка типов теряет смысл
class BookingDates(BaseModel):
    checkin: StrictStr
    checkout: StrictStr


class BookingInfo(BaseModel):
    firstname: StrictStr
    lastname: StrictStr
    totalprice: StrictInt
    depositpaid: StrictBool
    bookingdates: BookingDates
    additionalneeds: Optional[StrictStr] = None  # поле необязательное


class CreateBookingResponse(BaseModel):
    bookingid: StrictInt
    booking: BookingInfo