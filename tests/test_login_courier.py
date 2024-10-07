import requests
import pytest
import allure
from data.URL import url
from data.courier_data import register_new_courier_and_return_login_password

@pytest.fixture
def delete_courier_data():
    login_pass = register_new_courier_and_return_login_password()
    yield {
        "login": login_pass[0],
        "password": login_pass[1]
    }
    response = requests.post(f"{url}/api/v1/courier/login", data=login_pass)
    if response.status_code == 200:
        courier_id = response.json().get("id")
        if courier_id:
            requests.delete(f"{url}/api/v1/courier/{courier_id}")


class TestLoginCourier:
    @allure.title('Авторизация курьера')
    @allure.description('Проверка получения ID курьера при авторизации с корректным login и password (код - 200 и ID')
    def test_get_courier_id(self, delete_courier_data):
        payload = delete_courier_data
        response = requests.post(f"{url}/api/v1/courier/login", data=payload)

        assert response.status_code == 200
        assert 'id' in response.json()

    @allure.title('Авторизация курьера не пройдена при отправке неверного password')
    @allure.description('Проверка отправки неверного password при автроизации курьера (код - 404 и "message": "Учетная запись не найдена"')
    def test_get_courier_id(self):
        login_pass = register_new_courier_and_return_login_password()
        payload = {
            "login": login_pass[0],
            "password": login_pass[0]
        }
        response = requests.post(f"{url}/api/v1/courier/login", data=payload)

        assert response.status_code == 404
        assert response.json() == {"code": 404, "message": "Учетная запись не найдена"}, "Неверное содержимое ответа."

    @allure.title('Авторизация курьера не пройдена при отправке не всех обязательных полей')
    @allure.description(
        'Проверка авторизации курьера без обязательного поля- password (код - 400 и "message": ""message":  "Недостаточно данных для входа"')
    def test_login_courier_without_password(self):
        login_pass = register_new_courier_and_return_login_password()
        payload = {
            "login": login_pass[0],
            "password": ""
        }
        response = requests.post(f"{url}/api/v1/courier/login", data=payload)

        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для входа"}