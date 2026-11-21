from typing import Dict, Any, List, Optional
from fastapi import HTTPException
from datetime import date
from ..repositories import Cprepository
from ..validator import Cpaymnetvalidator

class Cpservice:
    def __init__(self, db):
        self.db = db
        self.repository = Cprepository(db)
        self.validator = Cpaymnetvalidator(self.repository)

    @staticmethod
    def _public(db_payment) -> Dict[str, Any]:
        return {
            "id": db_payment.платежи_id,
            "order": db_payment.заказы,
            "price": db_payment.цена,
            "method": db_payment.метод,
            "status": db_payment.статус,
            "date": db_payment.дата
        }

    def Sget_all(self) -> List[Dict[str, Any]]:
        return [self._public(pay) for pay in self.repository.get_all()]

    def Ssearch(self, платежи_id: Optional[int], заказы_id: Optional[int], статус_id: Optional[int], метод_id: Optional[int], дата_от: Optional[date], дата_до: Optional[date]):
        db_payment = self.repository.search(платежи_id, заказы_id, статус_id, метод_id, дата_от, дата_до)

        return [self._public(pay) for pay in db_payment]
    
    def Screate_payment(self, paymentdata: Dict[str, Any]):
        valid_data = self.validator.validate_create_payment(paymentdata)

        db_payment_data = {
            "order": paymentdata["заказы"],
            "price": paymentdata["цена"],
            "method": paymentdata["метод"],
            "status": paymentdata["статус"],
            "date": valid_data["дата"]
        }

        db_payment = self.repository.create_payment(db_payment_data)

        return {
            "message": "Платеж создан",
            "payment": self._public(db_payment)
        }

    def Supdate_payment(self, платежи_id: int, updatepaymentdata: Dict[str, Any]):

        valid_data = self.validator.validate_update_payment(updatepaymentdata)

        db_payment_update_data: Dict[str, Any] = {}

        if "заказы" in updatepaymentdata:
            db_payment_update_data["order"] = updatepaymentdata["заказы"]
        if "цена" in updatepaymentdata:
            db_payment_update_data["price"] = updatepaymentdata["цена"]
        if "метод" in updatepaymentdata:
            db_payment_update_data["method"] = updatepaymentdata["метод"]
        if "статус" in updatepaymentdata:
            db_payment_update_data["status"] = updatepaymentdata["статус"]
        if "дата" in updatepaymentdata:
            db_payment_update_data["date"] = valid_data["дата"]

        db_payment = self.repository.update_payment(платежи_id, db_payment_update_data)

        return {
            "message": "Платеж обновлен",
            "payment": self._public(db_payment)
        }

    def Sdelete_payment(self, платежи_id: int):

        self.repository.delete_payment(платежи_id)

        return {
            "message": "Платеж уален"
        }