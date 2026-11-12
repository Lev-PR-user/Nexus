from data import equipment_data
from data_def import _register_and_login
from data import user_data, user_login_number, user_data_m, user_data_o, user_data_c


def test_get_equipment_by_id(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Оборудование создано"

    equipment_id = response.json()["equipment"]["id"]

    get_res_id = client.get(
        "/omequipments/equipment_search",
        params={"оборудование_id": equipment_id},
        headers=headers
    )

    assert get_res_id.status_code == 200
    item = get_res_id.json()[0] if isinstance(get_res_id.json(), list) else get_res_id.json()
    assert item["id"] == equipment_id


def test_get_equipment_by_model(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Оборудование создано"

    equipment_id = response.json()["equipment"]["id"]
    equipment_model = equipment_data["модель"]

    get_res_model = client.get(
        "/omequipments/equipment_search",
        params={"модель": equipment_model},
        headers=headers
    )

    assert get_res_model.status_code == 200
    items = get_res_model.json() if isinstance(get_res_model.json(), list) else [get_res_model.json()]
    assert any(item["id"] == equipment_id for item in items)
    assert all(item["model"] == equipment_model for item in items)


def test_get_equipment_by_series(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Оборудование создано"

    equipment_id = response.json()["equipment"]["id"]
    equipment_series = equipment_data["серия"]

    get_res_series = client.get(
        "/omequipments/equipment_search",
        params={"серия": equipment_series},
        headers=headers
    )

    assert get_res_series.status_code == 200
    items = get_res_series.json() if isinstance(get_res_series.json(), list) else [get_res_series.json()]
    assert any(item["id"] == equipment_id for item in items)
    assert all(item["series"] == equipment_series for item in items)


def test_get_equipment_without_params(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    get_res = client.get("/omequipments/equipment_search", headers=headers)

    assert get_res.status_code == 400


def test_get_equipment_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    get_res = client.get(
        "/omequipments/equipment_search",
        params={"оборудование_id": 999999},
        headers=headers
    )

    assert get_res.status_code == 400


def test_get_all_equipments(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    e_id = response.json()["equipment"]["id"]

    get_res = client.get("/omequipments/equipments", headers=headers)

    assert get_res.status_code == 200
    items = get_res.json() if isinstance(get_res.json(), list) else [get_res.json()]
    assert any(item["id"] == e_id for item in items)


def test_get_equipments_without_token(client):
    response = client.get("/omequipments/equipments")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_equipment_without_token(client):
    response = client.post(
        "/aequipments/create_equipment",
        json=equipment_data
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_equipment(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Оборудование создано"
    assert response.json()["equipment"]["model"] == equipment_data["модель"]
    assert response.json()["equipment"]["series"] == equipment_data["серия"]
    assert response.json()["equipment"]["status"] == equipment_data["статус"]
    assert response.json()["equipment"]["location"] == equipment_data["расположение"]


def test_create_equipment_empty(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/aequipments/create_equipment",
        json={},
        headers=headers
    )

    assert response.status_code == 400
    assert "обязательно для заполнения" in response.json()["detail"]


def test_update_equipment(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    equipment_id = response.json()["equipment"]["id"]

    update_res = client.put(
        "/aequipments/update_equipment",
        params={"оборудование_id": equipment_id},
        json={
            "модель": "Sdt",
            "серия": "345wd",
            "статус": 3,
            "расположение": 2
        },
        headers=headers
    )

    assert update_res.status_code == 200
    assert update_res.json()["message"] == "оборудование обновлено"
    assert update_res.json()["equipment"] == {
        "id": equipment_id, 
        "model": "Sdt",
        "series": "345wd",
        "status": 3,
        "location": 2
    }


def test_update_equipment_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    equipment_id = response.json()["equipment"]["id"]

    update_res = client.put(
        "/aequipments/update_equipment",
        params={"оборудование_id": equipment_id},
        json={"модель": "x"}
    )

    assert update_res.status_code == 401
    assert update_res.json()["detail"] == "Not authenticated"


def test_update_equipment_not_found(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    update_res = client.put(
        "/aequipments/update_equipment",
        params={"оборудование_id": 999999},
        json={"модель": "x"},
        headers=headers
    )

    assert update_res.status_code == 500


def test_update_status_equipment(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    equipment_id = response.json()["equipment"]["id"]

    update_res = client.patch(
        "/omequipments/update_status",
        params={
            "оборудование_id": equipment_id,
            "статус_уведомления_id": 3
        },
        headers=headers
    )

    assert update_res.status_code == 200
    assert update_res.json()["equipment"]["status"] == 3


def test_update_status_equipment_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    equipment_id = response.json()["equipment"]["id"]

    update_res = client.patch(
        "/omequipments/update_status",
        params={
            "оборудование_id": equipment_id,
            "статус_уведомления_id": 3
        }
    )

    assert update_res.status_code == 401
    assert update_res.json()["detail"] == "Not authenticated"


def test_delete_equipment(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    equipment_id = response.json()["equipment"]["id"]

    delete_res = client.delete(
        "/aequipments/delete_equipment",
        params={"оборудование_id": equipment_id},
        headers=headers
    )

    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Оборудование удалено"


def test_delete_equipment_without_token(client):
    user, headers = _register_and_login(client, user_data, user_login_number)

    response = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    equipment_id = response.json()["equipment"]["id"]

    delete_res = client.delete(
        "/aequipments/delete_equipment",
        params={"оборудование_id": equipment_id}
    )

    assert delete_res.status_code == 401
    assert delete_res.json()["detail"] == "Not authenticated"

def test_get_equipments_as_manager(client):
    admin, admin_headers = _register_and_login(client, user_data, user_login_number)
    e_res = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=admin_headers
    )
    e_id = e_res.json()["equipment"]["id"]

    user, headers = _register_and_login(client, user_data_m, user_data_m)

    get_res = client.get("/omequipments/equipments", headers=headers)

    assert get_res.status_code == 200
    items = get_res.json() if isinstance(get_res.json(), list) else [get_res.json()]
    assert any(item["id"] == e_id for item in items)

def test_get_equipment_by_id_as_manager(client):
    admin, admin_headers = _register_and_login(client, user_data, user_login_number)
    e_res = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=admin_headers
    )
    e_id = e_res.json()["equipment"]["id"]

    user, headers = _register_and_login(client, user_data_m, user_data_m)

    get_res = client.get(
        "/omequipments/equipment_search",
        params={"оборудование_id": e_id},
        headers=headers
    )

    assert get_res.status_code == 200
    item = get_res.json()[0] if isinstance(get_res.json(), list) else get_res.json()
    assert item["id"] == e_id


def test_create_equipment_as_manager(client):
    user, headers = _register_and_login(client, user_data_m, user_data_m)

    response = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    assert response.status_code == 403

def test_update_equipment_as_manager(client):
    admin, admin_headers = _register_and_login(client, user_data, user_login_number)
    e_res = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=admin_headers
    )
    e_id = e_res.json()["equipment"]["id"]

    user, headers = _register_and_login(client, user_data_m, user_data_m)

    update_res = client.put(
        "/aequipments/update_equipment",
        params={"оборудование_id": e_id},
        json={"модель": "нов_модель"},
        headers=headers
    )

    assert update_res.status_code == 403


def test_update_status_as_manager(client):
    admin, admin_headers = _register_and_login(client, user_data, user_login_number)
    e_res = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=admin_headers
    )
    e_id = e_res.json()["equipment"]["id"]

    user, headers = _register_and_login(client, user_data_m, user_data_m)

    update_res = client.patch(
        "/omequipments/update_status",
        params={"оборудование_id": e_id, "статус_уведомления_id": 3},
        headers=headers
    )

    assert update_res.status_code == 200
    assert update_res.json()["equipment"]["status"] == 3


def test_delete_equipment_as_manager(client):
    admin, admin_headers = _register_and_login(client, user_data, user_login_number)
    e_res = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=admin_headers
    )
    e_id = e_res.json()["equipment"]["id"]

    user, headers = _register_and_login(client, user_data_m, user_data_m)

    delete_res = client.delete(
        "/aequipments/delete_equipment",
        params={"оборудование_id": e_id},
        headers=headers
    )

    assert delete_res.status_code == 403

def test_get_equipments_as_operator(client):
    admin, admin_headers = _register_and_login(client, user_data, user_login_number)
    e_res = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=admin_headers
    )
    e_id = e_res.json()["equipment"]["id"]

    user, headers = _register_and_login(client, user_data_o, user_data_o)

    get_res = client.get("/omequipments/equipments", headers=headers)

    # оператор входит в ["админ","менеджер","оператор"] -> 200
    assert get_res.status_code == 200
    items = get_res.json() if isinstance(get_res.json(), list) else [get_res.json()]
    assert any(item["id"] == e_id for item in items)


def test_create_equipment_as_operator(client):
    user, headers = _register_and_login(client, user_data_o, user_data_o)

    response = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    assert response.status_code == 403


def test_update_status_as_operator(client):
    admin, admin_headers = _register_and_login(client, user_data, user_login_number)
    e_res = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=admin_headers
    )
    e_id = e_res.json()["equipment"]["id"]

    user, headers = _register_and_login(client, user_data_o, user_data_o)

    update_res = client.patch(
        "/omequipments/update_status",
        params={"оборудование_id": e_id, "статус_уведомления_id": 3},
        headers=headers
    )

    # оператору можно менять статус
    assert update_res.status_code == 200
    assert update_res.json()["equipment"]["status"] == 3


def test_update_equipment_as_operator(client):
    admin, admin_headers = _register_and_login(client, user_data, user_login_number)
    e_res = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=admin_headers
    )
    e_id = e_res.json()["equipment"]["id"]

    user, headers = _register_and_login(client, user_data_o, user_data_o)

    update_res = client.put(
        "/aequipments/update_equipment",
        params={"оборудование_id": e_id},
        json={"модель": "нов_модель"},
        headers=headers
    )

    assert update_res.status_code == 403

def test_get_equipments_as_client(client):
    user, headers = _register_and_login(client, user_data_c, user_data_c)

    get_res = client.get("/omequipments/equipments", headers=headers)

    assert get_res.status_code == 403


def test_create_equipment_as_client(client):
    user, headers = _register_and_login(client, user_data_c, user_data_c)

    response = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=headers
    )

    assert response.status_code == 403


def test_update_status_as_client(client):
    admin, admin_headers = _register_and_login(client, user_data, user_login_number)
    e_res = client.post(
        "/aequipments/create_equipment",
        json=equipment_data,
        headers=admin_headers
    )
    e_id = e_res.json()["equipment"]["id"]

    user, headers = _register_and_login(client, user_data_c, user_data_c)

    update_res = client.patch(
        "/omequipments/update_status",
        params={"оборудование_id": e_id, "статус_уведомления_id": 3},
        headers=headers
    )

    assert update_res.status_code == 403