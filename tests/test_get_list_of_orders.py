import requests
import allure
from data.URL import url

class TestGetListOfOrders:


    @allure.title('Получение списка заказов')
    @allure.description('Получение списка заказов (код - 200 и "orders" в ответе)')
    def test_get_list_of_orders(self):

        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": "BLACK"
        }

        requests.post(f"{url}/api/v1/orders", json=payload)
        r = requests.get(f"{url}/api/v1/orders")
        assert r.status_code == 200
        assert 'orders' in r.json()