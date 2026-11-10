import requests

TIMEOUT = 10  # сколько секунд ждём ответ сервера


class Reservation:
    """Клиент Restful-booker API с авторизацией по токену."""

    def __init__(self, base_url, creds):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        token = self.get_token(creds)
        self.session.headers.update({"Cookie": f"token={token}"})

    def create_token(self, creds):
        """POST /auth - возвращает сырой ответ (нужен для тестов авторизации)."""
        return requests.post(f"{self.base_url}/auth", json=creds, timeout=TIMEOUT)

    def get_token(self, creds):
        """Возвращает токен или бросает ошибку, если логин/пароль неверные."""
        body = self.create_token(creds).json()
        if "token" not in body:
            raise RuntimeError(f"Не удалось получить токен, ответ сервера: {body}")
        return body["token"]

    def create_booking(self, payload):
        return self.session.post(f"{self.base_url}/booking", json=payload, timeout=TIMEOUT)

    def get_booking(self, booking_id):
        return self.session.get(f"{self.base_url}/booking/{booking_id}", timeout=TIMEOUT)

    def get_booking_ids(self):
        return self.session.get(f"{self.base_url}/booking", timeout=TIMEOUT)

    def update_booking(self, booking_id, payload):
        """PUT - заменить бронь целиком."""
        return self.session.put(f"{self.base_url}/booking/{booking_id}", json=payload, timeout=TIMEOUT)

    def partial_update_booking(self, booking_id, payload):
        """PATCH - изменить только переданные поля."""
        return self.session.patch(f"{self.base_url}/booking/{booking_id}", json=payload, timeout=TIMEOUT)

    def delete_booking(self, booking_id):
        return self.session.delete(f"{self.base_url}/booking/{booking_id}", timeout=TIMEOUT)


class ReservationWithoutAuth(Reservation):
    """Тот же клиент, но без токена - для проверки доступа без авторизации."""

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})