import requests
from data.URL import url

@pytest.fixture(scope="function", autouse=True)
def cleanup_function():
    yield
    # Выполняется после каждого теста
    # Авторизация и удаление курьера
    login_response = requests.post(f"{url}/api/v1/courier/login", data={
        "login": "test_courier", # Вставьте логин тестового курьера
        "password": "test_password" # Вставьте пароль тестового курьера
    })
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        if courier_id:
            requests.delete(f"{url}/api/v1/courier/{courier_id}")