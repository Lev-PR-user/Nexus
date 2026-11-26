from typing import Dict, Any
from fastapi import HTTPException
from datetime import datetime 
from ..repositories import Cnotification

class Cnotificationvalidator():
    def __init__(self, repository: Cnotification):
        self.repository = repository

    def validate_create_notification(self, notificationdata: Dict[str, Any]):
        required_fields = ["пользователь", "категория_уведомления", "канал_уведомления", "статус", "дата_отправки"]

        for field in required_fields:
            if field not in notificationdata or notificationdata[field] is None:
                raise HTTPException(status_code=400, detail=f"Поля {field} обязательны для заполнения")

        parsed_data = notificationdata.copy()

        if isinstance(parsed_data["дата_отправки"], str):
            try: 
                parsed_data["дата_отправки"] = datetime.strptime(parsed_data["дата_отправки"], "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Неверный формат даты") 

        user = parsed_data["пользователь"]

        existing_user = self.repository.get_user_by_id(user)

        if existing_user is None:
            raise HTTPException(status_code=400, detail="Такого пользователя нет")

        category = parsed_data["категория_уведомления"]

        existing_category = self.repository.get_notification_category_by_id(category)

        if existing_category is None:
            raise HTTPException(status_code=400, detail="Такой категории нет")

        channel = parsed_data["канал_уведомления"]

        existing_channel = self.repository.get_notification_channel_by_id(channel)

        if existing_channel is None:
            raise HTTPException(status_code=400, detail="Такого канала нет")

        status = parsed_data["статус"]

        existing_status = self.repository.get_notification_status_by_id(status)

        if existing_status is None:
            raise HTTPException(status_code=400, detail="Такого статус нет")

        return parsed_data