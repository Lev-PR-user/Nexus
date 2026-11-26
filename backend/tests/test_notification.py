from data import user_data, user_login_number, user_data_m, user_data_o, user_data_c
from data_def import _register_and_login


def test_create_notification_channel(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    
    response = client.post(
        "/channel_notification/create_channe_notification",
        json={"канал": "Email"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["channel"]["channel"] == "Email"


def test_create_notification_channel_empty(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    
    response = client.post(
        "/channel_notification/create_channe_notification",
        json={},
        headers=headers
    )
    assert response.status_code == 500


def test_get_all_notification_channels(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    
    response = client.get(
        "/channel_notification/get_all_channe", 
        headers=headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_notification_channel(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    
    res = client.post(
        "/channel_notification/create_channe_notification",
        json={"канал": "SMS"},
        headers=headers
    )
    ch_id = res.json()["channel"]["id"]

    update_res = client.put(
        f"/channel_notification/update_channe_notification?канал_уведомления_id={ch_id}",
        json={"канал": "Telegram"},
        headers=headers
    )
    assert update_res.status_code == 200
    assert update_res.json()["channel"]["channel"] == "Telegram"


def test_delete_notification_channel(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    
    res = client.post(
        "/channel_notification/create_channe_notification",
        json={"канал": "Push"},
        headers=headers
    )
    ch_id = res.json()["channel"]["id"]

    delete_res = client.delete(
        f"/channel_notification/delete_channe_notification?канал_уведомления_id={ch_id}",
        headers=headers
    )
    assert delete_res.status_code == 200


def test_create_notification_category(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    
    response = client.post(
        "/categories_notification/create_category_notification",
        json={"категория": "Срочно"},
        headers=headers
    )
    assert response.status_code == 200


def test_get_all_notification_categories(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    
    response = client.get(
        "/categories_notification/get_all_category",
        headers=headers
    )
    assert response.status_code == 200


def test_update_notification_category(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    
    res = client.post(
        "/categories_notification/create_category_notification",
        json={"категория": "Инфо"},
        headers=headers
    )
    cat_id = res.json()["category"]["id"]

    update_res = client.put(
        f"/categories_notification/update_category_notification?категория_уведомления_id={cat_id}",
        json={"категория": "Важное"},
        headers=headers
    )

    print(update_res.json())
    assert update_res.status_code == 200


def test_delete_notification_category(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    
    res = client.post(
        "/categories_notification/create_category_notification",
        json={"категория": "Спам"},
        headers=headers
    )
    cat_id = res.json()["category"]["id"]

    delete_res = client.delete(
        f"/categories_notification/delete_category_notification?категория_уведомления_id={cat_id}",
        headers=headers
    )
    assert delete_res.status_code == 200


def test_create_status_notification(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    
    response = client.post(
        "/status_notifications/create_status_notifications",
        json={"статус": "Отправлено"},
        headers=headers
    )
    assert response.status_code == 200


def test_update_status_notification(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    
    res = client.post(
        "/status_notifications/create_status_notifications",
        json={"статус": "В ожидании"},
        headers=headers
    )
    status_id = res.json()["status"]["id"]

    update_res = client.put(
        f"/status_notifications/update_status_notifications?статус_оборудования_id={status_id}",
        json={"статус": "Прочитано"},
        headers=headers
    )
    assert update_res.status_code == 200


def test_delete_status_notification(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    
    res = client.post(
        "/status_notifications/create_status_notifications",
        json={"статус": "Удалено"},
        headers=headers
    )
    status_id = res.json()["status"]["id"]

    delete_res = client.delete(
        f"/status_notifications/delete_status_notification?статус_оборудования_id={status_id}",
        headers=headers
    )
    assert delete_res.status_code == 200


def _prepare_notification_deps(client, headers):
    ch_res = client.post("/channel_notification/create_channe_notification", json={"канал": "Email_test"}, headers=headers)
    channel_id = ch_res.json()["channel"]["id"]

    cat_res = client.post("/categories_notification/create_category_notification", json={"категория": "Срочно_test"}, headers=headers)
    category_id = cat_res.json()["category"]["id"]

    st_res = client.post("/status_notifications/create_status_notifications", json={"статус": "Отправлено_test"}, headers=headers)
    status_id = st_res.json()["status"]["id"]

    return channel_id, category_id, status_id


def test_create_notification(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    channel_id, category_id, status_id = _prepare_notification_deps(client, headers)

    response = client.post(
        "/notifications/notification_create",
        json={
            "пользователь": 1,
            "категория_уведомления": category_id,
            "канал_уведомления": channel_id,
            "статус": status_id,
            "дата_отправки": "2026-05-20"
        },
        headers=headers
    )
    assert response.status_code == 200, response.json()
    assert response.json()["notification"]["user"] == 1


def test_create_notification_invalid_user(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    channel_id, category_id, status_id = _prepare_notification_deps(client, headers)

    response = client.post(
        "/notifications/notification_create",
        json={
            "пользователь": 9999,
            "категория_уведомления": category_id,
            "канал_уведомления": channel_id,
            "статус": status_id,
            "дата_отправки": "2026-05-20"
        },
        headers=headers
    )
    assert response.status_code == 400
    assert "Такого пользователя нет" in response.json()["detail"]


def test_create_notification_invalid_date(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    channel_id, category_id, status_id = _prepare_notification_deps(client, headers)

    response = client.post(
        "/notifications/notification_create",
        json={
            "пользователь": 1,
            "категория_уведомления": category_id,
            "канал_уведомления": channel_id,
            "статус": status_id,
            "дата_отправки": "неверная_дата"
        },
        headers=headers
    )
    assert response.status_code == 400
    assert "Неверный формат даты" in response.json()["detail"]


def test_get_all_notifications(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    
    response = client.get("/notifications/notifications", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_notifications_by_user(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    
    response = client.get("/notifications/notifications_by_user?пользователь_id=1", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_notification(client):
    user, headers = _register_and_login(client, user_data, user_login_number)
    channel_id, category_id, status_id = _prepare_notification_deps(client, headers)

    res = client.post(
        "/notifications/notification_create",
        json={
            "пользователь": 1,
            "категория_уведомления": category_id,
            "канал_уведомления": channel_id,
            "статус": status_id,
            "дата_отправки": "2026-05-20"
        },
        headers=headers
    )
    notif_id = res.json()["notification"]["id"]

    delete_res = client.delete(
        f"/notifications/notification_delete?уведомление_id={notif_id}",
        headers=headers
    )
    assert delete_res.status_code == 200


def test_create_notification_without_token(client):
    response = client.post("/notifications/notification_create", json={})
    assert response.status_code == 401


def test_get_notifications_as_manager(client):
    login_data_m = {"номер": "79990000002", "пароль": "securepassword"}
    user, headers = _register_and_login(client, user_data_m, user_data_m)
    
    response = client.get("/notifications/notifications", headers=headers)
    assert response.status_code == 403


def test_get_notifications_as_operator(client):
    login_data_o = {"номер": "79990000003", "пароль": "securepassword"}
    user, headers = _register_and_login(client, user_data_o, user_data_o)
    
    response = client.get("/notifications/notifications", headers=headers)
    assert response.status_code == 403


def test_get_notifications_as_client(client):
    login_data_c = {"номер": "79990000004", "пароль": "securepassword"}
    user, headers = _register_and_login(client, user_data_c, user_data_c)
    
    response = client.get("/notifications/notifications", headers=headers)
    assert response.status_code == 403