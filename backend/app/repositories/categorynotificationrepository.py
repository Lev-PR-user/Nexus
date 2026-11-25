from typing import Dict, Any, Optional, List
from ..models import КатегорияУведомленияM
from sqlalchemy.orm import Session
from fastapi import HTTPException

class Ccategorynotificationrepository:

    def __init__(self, db: Session):
        self.db = db

    def get_category_notification_by_id(self, категория_уведомления_id: int) -> Optional[КатегорияУведомленияM]:
        try: 
            self.db.query(КатегорияУведомленияM).filter(КатегорияУведомленияM.категория_уведомления_id == категория_уведомления_id)
        except HTTPException:
            self.db.rollback()
            raise

    def get_all(self) -> List[КатегорияУведомленияM]:
        try:
            return self.db.query(КатегорияУведомленияM).all()
        except HTTPException:
            self.db.rollback()
            raise

    def create_category_notification(self, categorynotificationata: Dict[str, Any]) -> КатегорияУведомленияM:
        try:
            category_notification_db = КатегорияУведомленияM(
                категория=categorynotificationata["category"]
            )

            self.db.add(category_notification_db)

            self.db.commit()

            self.db.refresh(category_notification_db)

            return category_notification_db
        except HTTPException:
            self.db.rollback()
            raise

    def update_category_notification(self, категория_уведомления_id: int, updatecategorynotificationata: Dict[str, Any]) -> КатегорияУведомленияM:
        try:
            category_notification_db = self.get_category_notification_by_id(категория_уведомления_id)

            if category_notification_db is None:
                raise HTTPException(status_code=400, detail="Такой катеегории уведомления нет")

            if "category" in updatecategorynotificationata:
                category_notification_db.категория = updatecategorynotificationata["category"]

            self.db.commit()

            self.db.refresh(category_notification_db)

            return category_notification_db
        except HTTPException:
            self.db.rollback()
            raise 

    def delete_category_notification(self, категория_уведомления_id: int) -> bool:
        try:
            category_notification_db = self.get_category_notification_by_id(категория_уведомления_id)

            if category_notification_db is None:
                return False

            self.db.commit()

            self.db.refresh(category_notification_db)

            return True
        except HTTPException:
            self.db.rollback()
            raise