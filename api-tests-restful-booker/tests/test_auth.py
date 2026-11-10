import pytest

from tests.config import CREDS


@pytest.mark.smoke
def test_auth_valid_credentials(reservation_no_auth):
    response = reservation_no_auth.create_token(CREDS)
    assert response.status_code == 200, f"ожидался код 200, но сервер вернул: {response.status_code}"
    assert response.json()["token"], "токен пустой"


@pytest.mark.negative
@pytest.mark.parametrize("bad_creds", [
    {"username": "admin", "password": "wrong"},
    {"username": "nobody", "password": "password123"},
    {"username": "admin", "password": ""},
    {"username": "", "password": "password123"}
])
def test_auth_invalid_credentials(reservation_no_auth, bad_creds):
    response = reservation_no_auth.create_token(bad_creds)
    # особенность API: код ответа 200, но токена в ответе быть не должно
    assert response.status_code == 200, f"expected 200, {response.status_code} came: {response.text}"
    assert response.json().get("reason") == "Bad credentials", response.text
    assert "token" not in response.json(), f"токен выдан на неверные данные: {response.text}"
