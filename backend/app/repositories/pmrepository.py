from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import МетодыОплатыM

class Cpmrepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[МетодыОплатыM]:
        try:
            return self.db.query(МетодыОплатыM).all()
        except HTTPException:
            self.db.rollback()
            raise

    def method_by_id(self, метод_id: Optional[int]):
        try:
            if метод_id is None:
                return None
            return self.db.query(МетодыОплатыM).filter(МетодыОплатыM.метод_id == метод_id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")

    def method_by_method(self, метод: Optional[str]):
        try:
            if метод is None:
                return None
            return self.db.query(МетодыОплатыM).filter(МетодыОплатыM.метод == метод).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")  

    def create_method(self, methodpaymentdata: Dict[str, Any]) -> МетодыОплатыM:
        try:
            method_payment_db = МетодыОплатыM(
                метод=methodpaymentdata["method"]
            )

            self.db.add(method_payment_db)

            self.db.commit()

            self.db.refresh(method_payment_db)

            return method_payment_db

        except HTTPException:
            self.db.rollback()
            raise

    def update_method(self, метод: Optional[str], метод_id: Optional[int], updatemethodpaymentdata: Dict[str, Any]) -> МетодыОплатыM:
        try:
            method_payment_db = self.method_by_id(метод_id) or self.method_by_method(метод)

            if method_payment_db is None:
                 raise HTTPException(status_code=500, detail="Такой метод оплаты не найдена")

            if "method" in updatemethodpaymentdata:
                method_payment_db.метод = updatemethodpaymentdata["method"]

            self.db.commit()

            self.db.refresh(method_payment_db)

            return method_payment_db
            
        except HTTPException:
            self.db.rollback()
            raise

    def delete_method(self, метод: Optional[str], метод_id: Optional[int]) -> bool:
        try:
            method_payment_db = self.method_by_id(метод_id) or self.method_by_method(метод)

            if method_payment_db is None:
                return False

            self.db.delete(method_payment_db)

            self.db.commit()

            return True
        
        except HTTPException:
            self.db.rollback()
            raise