import requests
import allure
import pytest
from data.URL import url
from data.courier_data import generation_new_data_courier
from data.courier_data import register_new_courier_and_return_login_password
import conftest


class TestCreateCourier:

    @allure.title('Создание курьера')
    @allure.step('Проверка создания курьера (код - 201 и текст - "ok": True')
    def test_create_courier(self):

        data = generation_new_data_courier()

        payload = data

        response = requests.post(f"{url}/api/v1/courier", data=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}, "Неверное содержимое ответа."


    @allure.title('Создание курьера')
    @allure.description('Проверка создания курьера (код - 409 и текст - "message": "Этот логин уже используется"')
    def test_create_courier_duplicate_login(self):
        login_pass = register_new_courier_and_return_login_password()
        payload = {
            "login": login_pass[0],
            "password": login_pass[1],
            "firstName": login_pass[2]
        }
        response = requests.post(f"{url}/api/v1/courier", data=payload)

        assert response.status_code == 409
        assert response.json() == {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}, "Неверное содержимое ответа."


    @allure.title('Создание курьера')
    @allure.description(
        'Проверка заполнения не всех обязательных полей. Курьер не создан (код - 409 и текст - "message": "Этот логин уже используется"')
    def test_create_courier_without_firstName(self):
        data = generation_new_data_courier()  # Получаем словарь с данными

        # Используем полученные данные из словаря
        payload = {
            "login": data["login"],
            "firstName": data["firstName"]
        }

        response = requests.post(f"{url}/api/v1/courier", data=payload)

        assert response.status_code == 400
        assert response.json() == {"code": 400,
                                   "message": "Недостаточно данных для создания учетной записи"}, "Неверное содержимое ответа."