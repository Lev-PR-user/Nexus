from ..repositories import Cchannelnotification
from typing import Dict, Any, List
from fastapi import HTTPException

class Cchannelnotificationservice:
    def __init__(self, db):
        self.db = db
        self.repository = Cchannelnotification(db)

    @staticmethod
    def _public(db_channel):
        return {
            "id": db_channel.канал_уведомления_id,
            "channel": db_channel.канал
        }

    def get_all(self):
        return [self._public(ch) for ch in self.repository.get_all()]

    def Screate_channel(self, chndata: Dict[str, Any]) -> Dict[str, Any]:
        db_channel_data = {
            "channel": chndata["канал"]
        }

        db_channel = self.repository.create_channel_notification(db_channel_data)

        return {
            "message": "Успешно создан канал уведомлений",
            "channel": self._public(db_channel)
        }

    def Supdate_channel(self, канал_уведомления_id: int, updatechndata: Dict[str, Any]) -> Dict[str, Any]:

        db_channel_update_data = {}

        if "канал" in updatechndata:
            db_channel_update_data["channel"] = updatechndata["канал"]

        db_channel = self.repository.update_channel_notification(канал_уведомления_id, db_channel_update_data)
        
        return {
            "message": "Успешно обновлен канал уведомлений",
            "channel": self._public(db_channel)
        }

    def Sdelete_channel(self, канал_уведомления_id: int) -> Dict[str, Any]:

       self.repository.delete_channel_notification(канал_уведомления_id)

       return {
            "message": "Успешно удален канал уведомлений"
            }

