from data import order_data
from data_def import _register_and_login
from data import user_data, user_login_number, user_data_m, user_data_o, user_data_c


def test_get_orders_without_token(client):
    response = client.get("/orders/orders")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_order_without_token(client):
    response = client.post("/orders/order_create", json=order_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_orders_as_admin(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.get("/orders/orders", headers=headers)

    assert response.status_code == 200


def test_get_orders_as_manager(client):
    user, headers = _register_and_login(client, user_data_m, user_data_m)

    response = client.get("/orders/orders", headers=headers)

    assert response.status_code == 200


def test_get_orders_as_operator(client):
    user, headers = _register_and_login(client, user_data_o, user_data_o)

    response = client.get("/orders/orders", headers=headers)

    assert response.status_code == 200


def test_get_orders_as_client(client):
    user, headers = _register_and_login(client, user_data_c, user_data_c)

    response = client.get("/orders/orders", headers=headers)

    assert response.status_code == 200


def test_create_order_as_admin(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/orders/order_create",
        json=order_data,
        headers=headers
    )

    assert response.status_code ==  400


def test_get_order_by_id_as_admin(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.get(
        "/orders/order_search",
        params={"заказ_id": 999999},
        headers=headers
    )

    assert response.status_code == 500


def test_get_order_by_id_without_token(client):
    response = client.get(
        "/orders/order_search",
        params={"заказ_id": 1}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_delete_order_without_token(client):
    response = client.delete(
        "/orders/order_delete",
        params={"заказ_id": 1}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_update_status_without_token(client):
    response = client.patch(
        "/orders/order_update_status",
        params={"заказ_id": 1, "статус_заказа_id": 2}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"