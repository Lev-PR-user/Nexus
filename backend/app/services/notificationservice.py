from typing import Dict, Any, Optional, List
from fastapi import HTTPException
from ..repositories import Cnotification

class Cnotificationservice:
    def __init__(self, db):
        self.db = db
        self.repository = Cnotification(db)

    @staticmethod
    def _public(notification_db) -> Dict[str, Any]:
        return {
            "id": notification_db.уведомление_id,
            "user": notification_db.пользователь,
            "categoty": notification_db.категория_уведомления,
            "channel": notification_db.канал_уведомления,
            "status": notification_db.статус,
            "date": notification_db.дата_отправки
        }

    def Sget_all(self) -> List[Dict[str, Any]]:
        return [self._public(n) for n in self.repository.get_all()]

    def Sget_notification(self, уведомление_id: int):
        return self.repository.get_notification_by_id(уведомление_id)

    def Sget_by_user(self, пользователь: int):
        return self.repository.get_notification_by_user_id(пользователь)

    def create_notification(self, notificationdata: Dict[str, Any]) -> Dict[str, Any]:
        db_notification_data = {
            "user": notificationdata["пользователь"],
            "category": notificationdata["категория_уведомления"],
            "channel": notificationdata["канал_уведомления"],
            "status": notificationdata["статус"],
            "date": notificationdata["дата_отправки"]
        }

        db_notification = self.repository.create_notification(db_notification_data)

        return {
            "message": "Уведомление успешно создано",
            "notification": self._public(db_notification)
        }

    def Sdelete_notification(self, уведомление_id: int) -> Dict[str, Any]:
        self.repository.delete_notification(уведомление_id)

        return {
            "message": "Уведомление удалено"
        }