from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import КаналУведомленийM

class Cchannelnotification:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[КаналУведомленийM]:
        try:
            return self.db.query(КаналУведомленийM).all()
        except HTTPException:
            self.db.rollback()
            raise

    def get_channel_by_id(self, канал_уведомления_id: int) -> Optional[КаналУведомленийM]:
        try:
            return self.db.query(КаналУведомленийM).filter(КаналУведомленийM.канал_уведомления_id == канал_уведомления_id).first()
        except HTTPException:
            self.db.rollback()
            raise

    def create_channel_notification(self, chndata: Dict[str, Any]) -> КаналУведомленийM:
        try:
            channel_db = КаналУведомленийM(
                канал=chndata["channel"]
            )

            self.db.add(channel_db)

            self.db.commit()

            self.db.refresh(channel_db)

            return channel_db

        except HTTPException:
            self.db.rollback()
            raise

    def update_channel_notification(self, канал_уведомления_id: int, updatechndata: Dict[str, Any]) -> КаналУведомленийM:
        try:
            channel_db = self.get_channel_by_id(канал_уведомления_id)

            if channel_db is None:
                raise HTTPException(status_code=400, detail="Такого канала нет")

            if "channel" in updatechndata:
                channel_db.канал = updatechndata["channel_db"]

            self.db.commit()

            self.db.refresh(channel_db)

            return channel_db
            
        except HTTPException:
            self.db.rollback()
            raise

    def delete_channel_notification(self, канал_уведомления_id: int) -> bool:
        try:
            channel_db = self.get_channel_by_id(канал_уведомления_id)
            if channel_db is None:
                return False

            self.db.delete(channel_db)

            self.db.commit()

            return True

        except HTTPException:
            self.db.rollback()
            raise