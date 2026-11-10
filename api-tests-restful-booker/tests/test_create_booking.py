import pytest

from api.schemas import CreateBookingResponse
from tests.data import new_booking


# happy path
@pytest.mark.smoke
def test_create_booking(create_booking):
    # arrange
    payload = new_booking()

    # act
    response = create_booking(payload)

    # assert: статус-код
    assert response.status_code == 200, f"ожидался код 200, но сервер вернул: {response.status_code}"
    # assert: структура + типы
    CreateBookingResponse.model_validate(response.json())
    # assert: значения (сервер возвращает то, что мы отправили)
    assert response.json()["booking"] == payload


# создание брони с неправильным типом данных
@pytest.mark.negative
@pytest.mark.xfail(reason="BUG: сервер не валидирует тип данных")
@pytest.mark.parametrize("field, wrong_data_type", [
    ("totalprice", "not number"),
    ("depositpaid", "yes"),
    ("depositpaid", 98),
    ("firstname", 5623),
    ("lastname", 4643),
])
def test_create_booking_wrong_type(create_booking, field, wrong_data_type):
    payload = new_booking(**{field: wrong_data_type})
    response = create_booking(payload)
    assert response.status_code == 400, f"expected 400, {response.status_code} came"


# создание брони с невалидными данными
@pytest.mark.negative
@pytest.mark.xfail(reason="BUG: сервер не валидирует значения полей")
@pytest.mark.parametrize("field, invalid_data", [
    ("totalprice", -5),
    ("firstname", ""),
    ("lastname", ""),
    ("bookingdates", {}),
])
def test_create_booking_invalid_value(create_booking, field, invalid_data):
    payload = new_booking(**{field: invalid_data})
    response = create_booking(payload)
    assert response.status_code == 400, f"expected 400, {response.status_code} came"


# создание брони без обязательного поля
@pytest.mark.negative
@pytest.mark.xfail(reason="BUG: без обязательного поля сервер отвечает 500 вместо 400")
@pytest.mark.parametrize("required_field", [
    "firstname", "lastname", "totalprice", "depositpaid", "bookingdates",
])
def test_create_booking_without_required_field(create_booking, required_field):
    payload = new_booking()
    del payload[required_field]
    response = create_booking(payload)
    assert response.status_code == 400, f"expected 400, {response.status_code} came"