import pytest
from constants import BASE_URL


class TestBookings:
    def test_create_booking(self, auth_session, booking_data, new_booking_data, booking_data_negative):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"],\
            "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"],\
            "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"],\
            "Заданная фамилия не совпадает"

        #Полное изменение бронирования
        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=booking_data)
        assert put_booking.status_code == 200, "Бронь не изменена"

        #Получаем полностью измененный ресурс
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], \
            "Заданная фамилия не совпадает"
        assert get_booking.json()["firstname"] == booking_data["firstname"],\
            "Заданное имя не совпадает"

        #Частичное изменение бронирования
        patch_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=new_booking_data)
        assert patch_booking.status_code == 200, "Ресурс не изменен"

        #Получаем частично измененный ресурс
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == new_booking_data["lastname"], \
            "Заданная фамилия не совпадает"

        #Проверяем, что данные изменились и их можно получить
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["firstname"] == new_booking_data["firstname"], \
            "Заданное имя не совпадает"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"



        #Негативные кейсы
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data_negative)
        assert create_booking.status_code == 500, "Броня создана, вопреки ожидаемому результату"


        create_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json={})
        assert create_booking.status_code == 400, "Ресурс обновлен на пустой json"


        create_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json={})
        assert create_booking.status_code == 405, "Ресурс частично обновлен на пустой json"

