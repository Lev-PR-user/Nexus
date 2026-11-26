from typing import Dict, Optional, Any, List
from ..models import СтатусУведомленияM
from sqlalchemy.orm import Session
from fastapi import HTTPException

class Cstatusnotification:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[СтатусУведомленияM]:
        try:
            return self.db.query(СтатусУведомленияM).all()
        except HTTPException:
            self.db.rollback()
            raise

    def get_status_notification_by_id(self, статус_оборудования_id: int) -> Optional[СтатусУведомленияM]:
        try:
            return self.db.query(СтатусУведомленияM).filter(СтатусУведомленияM.статус_уведомления_id == статус_оборудования_id).first()
        except HTTPException:
            self.db.rollback()
            raise

    def create_status_notification(self, notificationdata: Dict[str, Any]) -> СтатусУведомленияM:
        try:
            status_n_db = СтатусУведомленияM(
                статус=notificationdata["status"]
            )

            self.db.add(status_n_db)

            self.db.commit()

            self.db.refresh(status_n_db)

            return status_n_db
        
        except HTTPException:
            self.db.rollback()
            raise

    def update_status_notification(self, статус_оборудования_id: int, updatenotificationdata: Dict[str, Any]) -> СтатусУведомленияM:
        try:
            update_status_n_db = self.get_status_notification_by_id(статус_оборудования_id)

            if update_status_n_db is None:
                raise HTTPException(status_code=400, detail="Такого статуса уведомления нет")

            if "status" in updatenotificationdata:
                update_status_n_db.статус = updatenotificationdata["status"]

            self.db.commit()

            self.db.refresh(update_status_n_db)

            return update_status_n_db
        except HTTPException:
            self.db.rollback()
            raise

    def delete_status_notification(self, статус_оборудования_id: int) -> bool:
        try:
            status_n_db = self.get_status_notification_by_id(статус_оборудования_id)

            if status_n_db is None:
                return False

            self.db.delete(status_n_db)

            self.db.commit()

            return True
        except HTTPException:
            self.db.rollback()
            raise