from typing import Dict, Any, Optional
from ..repositories import Cstatusnotification

class Cstatusnotification:
    def init(self, db):
        self.db = db
        self.repository = Cstatusnotification(db)

    @staticmethod
    def _public(db_notfication_status):
        return {
            "id": db_notfication_status.статус_уведомления_id,
            "status": db_notfication_status.статус
        }
    
    def get_all(self):
        return [self._public(ns) for ns in self.repository.get_all()]

    def Screate_notification(self, notificationdata: Dict[str, Any]) -> Dict[str, Any]:
        db_notification_data = {
            "status": notificationdata["статус"]
        }

        db_notfication_status = self.repository.create_status_notification(db_notification_data)

        return {
            "message": "Статус уведомления успешно создан",
            "status_notification": [self._public(db_notfication_status)]
        }

    def Supdate_status_notification(self, статус_оборудования_id: int, updatenotificationdata: Dict[str, Any]) -> Dict[str, Any]:
        db_notification_update_status_data = {}

        if "статус" in updatenotificationdata:
            db_notification_update_status_data["status"] = updatenotificationdata["статус"]

        db_notfication_status = self.repository.update_status_notification(статус_оборудования_id, db_notification_update_status_data)

        return {
            "message": "Статус успешно обновлен",
            "status_notification": [self._public(db_notfication_status)]
        }

    def Sdelete_status_notification(self, статус_оборудования_id: int) -> Dict[str, Any]:

        self.repository.delete_status_notification(статус_оборудования_id)

        return {
            "message": "Статус уведомления успешно удален"
        }