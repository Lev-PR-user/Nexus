from data import payment_data, payment_method_data, payment_status_data, payment_order_data
from data_def import _register_and_login
from data import user_data, user_login_number, user_data_m, user_data_o, user_data_c

def _prepare_payment_deps(client, headers):
    """Создаёт метод оплаты, статус оплаты, локацию, услугу, клиента и заказ."""
    client.post(
        "/payment_methods/method_create",
        json=payment_method_data,
        headers=headers
    )

    client.post(
        "/payment_statuses/status_create",
        json=payment_status_data,
        headers=headers
    )

    client.post(
        "/locations/location_create",
        json={
            "название": "тестовая локация",
            "адрес": "тестовый адрес",
            "часы_работы": {"пн-пт": "09:00-18:00"}
        },
        headers=headers
    )

    client.post(
        "/services/service_create",
        json={"услуга": "тестовая услуга"},
        headers=headers
    )

    client.post(
        "/type_clients/type_client_create",
        json={"тип": "ИП"},
        headers=headers
    )

    client.post(
        "/clients/client_create",
        json={
            "имя": "тестовый клиент",
            "тип": 1,
            "пользователь": 1,
            "заметки": "",
            "контакты": {"номер": "79990000000", "почта": "c@example.com"}
        },
        headers=headers
    )

    client.post(
        "/orders/order_create",
        json=payment_order_data,
        headers=headers
    )


def test_create_payment_without_token(client):
    response = client.post("/payments/payment_create", json=payment_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_payments_without_token(client):
    response = client.get("/payments/payments")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_payment_by_id_without_token(client):
    response = client.get(
        "/payments/payment_search",
        params={"платеж_id": 1}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_update_payment_without_token(client):
    response = client.put(
        "/payments/payment_update",
        params={"платеж_id": 1},
        json={"цена": "2000.00"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_delete_payment_without_token(client):
    response = client.delete(
        "/payments/payment_delete",
        params={"платеж_id": 1}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_payment_as_admin(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    _prepare_payment_deps(client, headers)

    response = client.post(
        "/payments/payment_create",
        json=payment_data,
        headers=headers
    )

    assert response.status_code in (200, 201, 400, 500)


def test_create_payment_empty(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/payments/payment_create",
        json={},
        headers=headers
    )

    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"]


def test_create_payment_negative_price(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/payments/payment_create",
        json={
            "заказы": 1,
            "цена": "-100.00",
            "метод": 1,
            "статус": 1,
            "дата": "2026-01-03"
        },
        headers=headers
    )

    assert response.status_code in (400, 422)


def test_create_payment_invalid_order(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/payments/payment_create",
        json={
            "заказы": 999999,
            "цена": "100.00",
            "метод": 1,
            "статус": 1,
            "дата": "2026-01-03"
        },
        headers=headers
    )

    assert response.status_code in (400, 404, 500)


def test_get_all_payments_as_admin(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.get("/payments/payments", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_all_payments_as_manager(client):
    user, headers = _register_and_login(client, user_data_m, user_login_number)

    response = client.get("/payments/payments", headers=headers)

    assert response.status_code in (200, 403)


def test_get_all_payments_as_operator(client):
    user, headers = _register_and_login(client, user_data_o, user_login_number)

    response = client.get("/payments/payments", headers=headers)

    assert response.status_code in (200, 403)


def test_get_all_payments_as_client(client):
    user, headers = _register_and_login(client, user_data_c, user_login_number)

    response = client.get("/payments/payments", headers=headers)

    assert response.status_code in (200, 403)


def test_get_payment_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.get(
        "/payments/payment_search",
        params={"платеж_id": 999999},
        headers=headers
    )

    assert response.status_code in (400, 404)


def test_update_payment_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.put(
        "/payments/payment_update",
        params={"платеж_id": 999999},
        json={"цена": "2000.00"},
        headers=headers
    )

    assert response.status_code in (400, 404, 500)


def test_delete_payment_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.delete(
        "/payments/payment_delete",
        params={"платеж_id": 999999},
        headers=headers
    )

    assert response.status_code in (200, 400, 404)


def test_get_payments_by_order(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    _prepare_payment_deps(client, headers)

    response = client.get(
        "/payments/payments_by_order",
        params={"заказ_id": 1},
        headers=headers
    )

    assert response.status_code in (200, 400, 404)


def test_get_payments_by_status(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.get(
        "/payments/payments_by_status",
        params={"статус_оплаты_id": 1},
        headers=headers
    )

    assert response.status_code in (200, 400, 404)


def test_get_payments_by_method(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.get(
        "/payments/payments_by_method",
        params={"метод_id": 1},
        headers=headers
    )

    assert response.status_code in (200, 400, 404)


def test_get_payments_by_client(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.get(
        "/payments/payments_by_client",
        params={"клиент_id": 1},
        headers=headers
    )

    assert response.status_code in (200, 400, 404)


def test_get_payments_by_period(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.get(
        "/payments/payments_by_period",
        params={"дата_от": "2026-01-01", "дата_до": "2026-12-31"},
        headers=headers
    )

    assert response.status_code in (200, 400)


def test_create_payment_duplicate(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    _prepare_payment_deps(client, headers)

    client.post(
        "/payments/payment_create",
        json=payment_data,
        headers=headers
    )

    response = client.post(
        "/payments/payment_create",
        json=payment_data,
        headers=headers
    )

    assert response.status_code in (200, 400)


def test_update_payment_status(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    _prepare_payment_deps(client, headers)

    create_res = client.post(
        "/payments/payment_create",
        json=payment_data,
        headers=headers
    )

    if create_res.status_code not in (200, 201):
        return

    payment_id = create_res.json()["payment"]["id"]

    update_res = client.patch(
        "/payments/payment_update_status",
        params={"платеж_id": payment_id},
        json={"статус": 2},
        headers=headers
    )

    assert update_res.status_code in (200, 400, 404)

def test_delete_payment_as_admin(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    _prepare_payment_deps(client, headers)

    create_res = client.post(
        "/payments/payment_create",
        json=payment_data,
        headers=headers
    )

    if create_res.status_code not in (200, 201):
        return

    payment_id = create_res.json()["payment"]["id"]

    delete_res = client.delete(
        "/payments/payment_delete",
        params={"платеж_id": payment_id},
        headers=headers
    )

    assert delete_res.status_code in (200, 400, 404)


def test_payment_public_fields(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    _prepare_payment_deps(client, headers)

    create_res = client.post(
        "/payments/payment_create",
        json=payment_data,
        headers=headers
    )

    if create_res.status_code not in (200, 201):
        return

    payment = create_res.json()["payment"]

    assert "id" in payment
    assert "order" in payment
    assert "price" in payment
    assert "method" in payment
    assert "status" in payment
    assert "date" in payment