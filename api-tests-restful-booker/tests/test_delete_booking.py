import pytest


@pytest.mark.smoke
def test_delete_booking(reservation, created_booking):
    response = reservation.delete_booking(created_booking["id"])
    # особенность API: успешное удаление возвращает 201
    assert response.status_code == 201, f"ожидался код 201, но сервер вернул: {response.status_code}"
    # бронь действительно удалена
    assert reservation.get_booking(created_booking["id"]).status_code == 404


@pytest.mark.negative
def test_delete_booking_without_auth(reservation, reservation_no_auth, created_booking):
    response = reservation_no_auth.delete_booking(created_booking["id"])
    assert response.status_code == 403, f"expected 403, {response.status_code} came"
    # бронь на месте
    assert reservation.get_booking(created_booking["id"]).status_code == 200