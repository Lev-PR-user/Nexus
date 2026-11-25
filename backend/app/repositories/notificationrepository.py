from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import УведомленияM

class Cnotification:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[УведомленияM]:
        try:
            return self.db.query(УведомленияM).all()
        except HTTPException:
            self.db.rollback()
            raise

    def get_notification_by_id(self, уведомление_id: int) -> Optional[УведомленияM]:
        try:
            return self.db.query(УведомленияM).filter(УведомленияM.уведомление_id == уведомление_id).first()
        except HTTPException:
            self.db.rollback()
            raise

    def get_notification_by_user_id(self, пользователь: int) -> Optional[УведомленияM]:
        try:
            return self.db.query(УведомленияM).filter(УведомленияM.пользователь == пользователь).first()
        except HTTPException:
            self.db.rollback()
            raise

    def create_notification(self, notificationdata: Dict[str, Any]) -> УведомленияM:
        try:
            notification_db = УведомленияM(
                пользователь=notificationdata["user"],
                категория_уведомления=notificationdata["category"],
                канал_уведомления=notificationdata["channel"],
                статус=notificationdata["status"],
                дата_отправки=notificationdata["send_date"]
            )

            self.db.add(notification_db)

            self.db.commit()

            self.db.refresh(notification_db)

            return notification_db
        
        except HTTPException:
            self.db.rollback()
            raise

    def delete_notification(self, уведомление_id: int) -> bool:
        try:
            notification_db = self.get_notification_by_id(уведомление_id)

            if notification_db is None:
                return False

            self.db.delete(notification_db)

            self.db.commit()

            return True

        except HTTPException:
            self.db.rollback()
            raise