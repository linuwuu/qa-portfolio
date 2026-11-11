import pytest

from tests.data import new_booking


@pytest.mark.smoke
def test_update_booking_put(reservation, created_booking):
    new_data = new_booking(firstname="Jim", lastname="Beam", totalprice=222)
    response = reservation.update_booking(created_booking["id"], new_data)
    assert response.status_code == 200, f"ожидался код 200, но сервер вернул: {response.status_code}"
    assert response.json() == new_data
    # проверяем, что изменения реально сохранились
    assert reservation.get_booking(created_booking["id"]).json() == new_data


def test_update_booking_patch(reservation, created_booking):
    changes = {"firstname": "Updated", "totalprice": 999}
    response = reservation.partial_update_booking(created_booking["id"], changes)
    assert response.status_code == 200, f"ожидался код 200, но сервер вернул: {response.status_code}"
    # поменялись только переданные поля, остальные остались прежними
    assert response.json() == {**created_booking["payload"], **changes}
    saved_response = reservation.get_booking(created_booking["id"])
    assert saved_response.status_code == 200, saved_response.text
    assert saved_response.json() == {**created_booking["payload"], **changes}


@pytest.mark.negative
def test_update_booking_without_auth(reservation, reservation_no_auth, created_booking):
    response = reservation_no_auth.update_booking(created_booking["id"], new_booking(firstname="Hacker"))
    assert response.status_code == 403, f"expected 403, {response.status_code} came"
    # данные не изменились
    assert reservation.get_booking(created_booking["id"]).json() == created_booking["payload"]
