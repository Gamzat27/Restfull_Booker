import pytest
import requests
from faker import Faker
from constants import HEADERS, BASE_URL

faker = Faker() #Объект класса Faker

#Позитив
@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    response = requests.post(
        f"{BASE_URL}/auth",
        headers=HEADERS,
        json={"username": "admin", "password": "password123"}
    )
    assert response.status_code == 200, "Ошибка авторизации"
    token = response.json().get("token")
    assert token is not None, "В ответе не оказалось токена"

    session.headers.update({"Cookie": f"token={token}"})
    return session

#Позитив
@pytest.fixture
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Cigars"
    }

#Позитив
@pytest.fixture
def new_booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=157700, max=350000),
        "depositpaid": faker.boolean(),
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Пианино и ноутбук, чтобы писать автотесты."
    }

#Негатив
@pytest.fixture()
def booking_data_negative():
    return {
        "firstname": [],
        "lastname": "",
        "totalprice": "100000",
        "bookingdates": {
            "checkin": "05",
            "checkout": "2024"
        },
        "additionalneeds": 10
    }


