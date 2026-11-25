from typing import Dict, List, Any, Optional
from ..repositories import Ccategorynotificationrepository
from fastapi import HTTPException

class Ccategorynotificationservice:

    def __init__(self, db):
        self.db = db
        self.repository = Ccategorynotificationrepository(db)

    @staticmethod
    def _public(categorynotification_db) -> Dict[str, Any]:
        return{
            "id": categorynotification_db.категория_уведомления_id,
            "category": categorynotification_db.категория
        }

    def get_all(self):
        return [self._public(cs) for cs in self.repository.get_all()]
    
    def create_category_notification(self, categorynotificationata: Dict[str, Any]):

        db_notification_data = {
            "category": categorynotificationata["категория"]
        }

        db_category_notification = self.repository.create_category_notification(db_notification_data)

        return {
            "message": "Категория успешно создана",
            "category_notification": self. _public(db_category_notification)
        }

    def update_category_notfication(self, категория_уведомления_id: int, updatecategorynotificationata: Dict[str, Any]):

        db_category_notification_data ={}

        if "категория" in updatecategorynotificationata:
            db_category_notification_data["category"] = updatecategorynotificationata["категория"]

        db_category_notification = self.repository.update_category_notification(категория_уведомления_id, db_category_notification_data)

        return {
            "messaage": "Категория успешно обновлена",
            "category": self._public(db_category_notification)
        }

    def delete_category_notification(self, категория_уведомления_id: int):

        self.repository.delete_category_notification(категория_уведомления_id)

        return {
            "message": "Категория успешно удалена"
        }

