import pytest

from api.client import Reservation, ReservationWithoutAuth
from tests.config import BASE_URL, CREDS
from tests.data import new_booking


@pytest.fixture(scope="session")
def reservation():
    """Клиент с токеном (один на весь прогон)"""
    return Reservation(BASE_URL, CREDS)


@pytest.fixture(scope="session")
def reservation_no_auth():
    """Клиент без токена"""
    return ReservationWithoutAuth(BASE_URL)


@pytest.fixture
def create_booking(reservation):
    """Создаёт бронь и после теста сама её удаляет"""
    created_ids = []

    def _create(payload):
        response = reservation.create_booking(payload)
        if response.status_code == 200:
            created_ids.append(response.json()["bookingid"])
        return response

    yield _create

    for booking_id in created_ids:
        reservation.delete_booking(booking_id)


@pytest.fixture
def created_booking(create_booking):
    """Уже созданная бронь: возвращает её id и данные, с которыми она создана."""
    payload = new_booking()
    response = create_booking(payload)
    assert response.status_code == 200, f"бронь не создалась, статус код: {response.status_code}"
    return {"id": response.json()["bookingid"], "payload": payload}