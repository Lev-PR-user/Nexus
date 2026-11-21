from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal
from fastapi import HTTPException
from ..models import ПлатежиM, ЗаказыM, МетодыОплатыM, СтатусыОплатыM

class Cprepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ПлатежиM]:
        try:
            return self.db.query(ПлатежиM).all()
        except HTTPException:
            self.db.rollback()
            raise

    def get_payment_by_id(self, платежи_id: int):
        try:
            return self.db.query(ПлатежиM).filter(ПлатежиM.платежи_id == платежи_id).first()
        except HTTPException:
            self.db.rollback()
            raise

    def get_order_by_id(self, заказы: int):
        try:
            return self.db.query(ЗаказыM).filter(ЗаказыM.заказ_id == заказы).first()
        except HTTPException:
            self.db.rollback()
            raise

    def get_method_by_id(self, метод: int):
        try:
            return self.db.query(МетодыОплатыM).filter(МетодыОплатыM.метод_id == метод).first()
        except HTTPException:
            self.db.rollback()
            raise

    def duplicate_payment(self, метод: int, цена: Decimal, заказы: int ):
        try:
            return self.db.query(ПлатежиM).filter(
                ПлатежиM.метод == метод,
                ПлатежиM.цена == цена,
                ПлатежиM.заказы == заказы
            ).first()
        except HTTPException:
            self.db.rollback()
            raise

    def get_status_by_id(self, статус: int):
        try:
            return self.db.query(СтатусыОплатыM).filter(СтатусыОплатыM.статусы_оплаты_id == статус).first()
        except HTTPException:
            self.db.rollback()
            raise

    def search(self, платежи_id: Optional[int], заказы_id: Optional[int], статус_id: Optional[int], метод_id: Optional[int], дата_от: Optional[date], дата_до: Optional[date]):
        try:
            query = self.db.query(ПлатежиM)

            if платежи_id is not None:
                query = query.filter(ПлатежиM.платежи_id == платежи_id)
            if заказы_id is not None:
                query = query.filter(ПлатежиM.заказы == заказы_id)
            if статус_id is not None:
                query = query.filter(ПлатежиM.статус == статус_id)
            if метод_id is not None:
                query = query.filter(ПлатежиM.метод == метод_id)
            if дата_от is not None:
                query = query.filter(ПлатежиM.дата >= дата_от)
            if дата_до is not None:
                query = query.filter(ПлатежиM.дата <= дата_до)

            return query.all()
            
        except HTTPException:
            self.db.rollback()
            raise


    def create_payment(self, paymentdata: Dict[str, Any]) -> ПлатежиM:
        try:
            payment_db = ПлатежиM(
                заказы=paymentdata["order"],
                цена=paymentdata["price"],
                метод=paymentdata["method"],
                статус=paymentdata["status"],
                дата=paymentdata["date"],
            )

            self.db.add(payment_db)

            self.db.commit()

            self.db.refresh(payment_db)

            return payment_db

        except HTTPException:
            self.db.rollback()
            raise

    def update_payment(self, платежи_id: int, updatepaymentdata: Dict[str, Any]) -> ПлатежиM:
        try:
            payment_db = self.get_payment_by_id(платежи_id)

            if payment_db is None:
                raise HTTPException(status_code=404, detail="Платеж не найден")
            
            if "order" in updatepaymentdata:
                payment_db.заказы = updatepaymentdata["order"]
            if "price" in updatepaymentdata:
                payment_db.цена = updatepaymentdata["price"]
            if "method" in updatepaymentdata:
                payment_db.метод = updatepaymentdata["method"]
            if "status" in updatepaymentdata:
                payment_db.статус = updatepaymentdata["status"]
            if "date" in updatepaymentdata:
                payment_db.дата = updatepaymentdata["date"]

            self.db.commit()

            self.db.refresh(payment_db)

            return payment_db
        
        except HTTPException:
            self.db.rollback()
            raise

    def delete_payment(self, платежи_id: int) -> bool:
        try:
            payment_db = self.get_payment_by_id(платежи_id)

            if payment_db is None:
                return False

            self.db.delete(payment_db)

            self.db.commit()

            return True
        except HTTPException:
            self.db.rollback()
            raise