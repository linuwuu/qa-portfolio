from copy import deepcopy

BASE_BOOKING = {
    "firstname": "James",
    "lastname": "Brown",
    "totalprice": 111,
    "depositpaid": True,
    "bookingdates": {"checkin": "2018-01-01", "checkout": "2019-01-01"},
    "additionalneeds": "Breakfast",
}


def new_booking(**changes):
    """Валидная бронь; нужные поля можно подменить: new_booking(totalprice=-5)."""
    body = deepcopy(BASE_BOOKING)
    body.update(changes)
    return body