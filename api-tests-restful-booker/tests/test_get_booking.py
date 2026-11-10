import pytest

from api.schemas import BookingInfo


# happy path
@pytest.mark.smoke
def test_get_booking(reservation, created_booking):
    # act
    response = reservation.get_booking(created_booking["id"])

    # assert: статус-код
    assert response.status_code == 200, f"ожидался код 200, но сервер вернул: {response.status_code}"
    # assert: структура + типы
    BookingInfo.model_validate(response.json())
    # assert: значения
    assert response.json() == created_booking["payload"]


@pytest.mark.negative
@pytest.mark.parametrize("invalid_id", [-1, 0, 66666])
def test_get_booking_invalid_id(reservation, invalid_id):
    response = reservation.get_booking(invalid_id)
    assert response.status_code == 404, f"expected 404, {response.status_code} came"


def test_get_booking_ids_contains_created(reservation, created_booking):
    response = reservation.get_booking_ids()
    assert response.status_code == 200, f"ожидался код 200, но сервер вернул: {response.status_code}"
    all_ids = [item["bookingid"] for item in response.json()]
    assert created_booking["id"] in all_ids