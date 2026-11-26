from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import УведомленияM, КаналУведомленийM, КатегорияУведомленияM, СтатусУведомленияM, ПользователиM

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

    def get_notification_by_user_id(self, пользователь: int) -> List[УведомленияM]:
        try:
            return self.db.query(УведомленияM).filter(УведомленияM.пользователь == пользователь).all()
        except HTTPException:
            self.db.rollback()
            raise

    def get_notification_status_by_id(self, статус: int) -> Optional[СтатусУведомленияM]:
        try:
            return self.db.query(СтатусУведомленияM).filter(СтатусУведомленияM.статус_уведомления_id == статус).first()
        except HTTPException:
            self.db.rollback()
            raise

    def get_user_by_id(self, пользователь: int) -> Optional[ПользователиM]:
        try:
            return self.db.query(ПользователиM).filter(ПользователиM.пользователь_id == пользователь).first()
        except HTTPException:
            self.db.rollback()
            raise

    def get_notification_category_by_id(self, категория_уведомления: int) -> Optional[КатегорияУведомленияM]:
        try:
            return self.db.query(КатегорияУведомленияM).filter(КатегорияУведомленияM.категория_уведомления_id == категория_уведомления).first()
        except HTTPException:
            self.db.rollback()
            raise

    def get_notification_channel_by_id(self, канал_уведомления: int) -> Optional[КаналУведомленийM]:
        try:
            return self.db.query(КаналУведомленийM).filter(КаналУведомленийM.канал_уведомления_id == канал_уведомления).first()
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
                дата_отправки=notificationdata["date"]
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