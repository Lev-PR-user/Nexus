from typing import Dict, Any, List, Optional
from fastapi import HTTPException
from ..repositories import Cpmrepository

class Cpmservice:
    def __init__(self, db):
            self.db = db
            self.repository = Cpmrepository(db)

    @staticmethod
    def _public(db_method_payment) -> Dict[str, Any]:
          return {
                "id": db_method_payment.метод_id,
                "method": db_method_payment.метод
          }

    def Sget_all(self):
        return [self._public(pm) for pm in self.repository.get_all()]

    def Ssearch(self, метод: Optional[str], метод_id: Optional[int]):
        if метод: 
           db_method_payment = self.repository.method_by_method(метод)
        elif метод_id:
            db_method_payment = self.repository.method_by_id(метод_id)
        else:
            raise HTTPException(status_code=400, detail="Введите данные для поиска")

        if db_method_payment is None:
            raise HTTPException(status_code=400, detail="Такого метода оплаты нет")
        
        return self._public(db_method_payment)

    def Screate_method_payment(self, methodpaymentdata: Dict[str, Any]) -> Dict[str, Any]:
        db_method_payment_data = {
            "method": methodpaymentdata["метод"]
        }

        db_method_payment = self.repository.create_method(db_method_payment_data)

        return {
            "message": "Метод оплаты успешно создан",
            "method": self._public(db_method_payment)
        }

    def Supdate_method_payment(self, updatemethodpaymentdata: Dict[str, Any], метод: Optional[str], метод_id: Optional[int], ) -> Dict[str, Any]:
        db_method_payment_update_data = {}

        if "метод" in updatemethodpaymentdata:
           db_method_payment_update_data["method"] = updatemethodpaymentdata["метод"]

        db_method_payment_update = self.repository.update_method(метод, метод_id, db_method_payment_update_data)

        return {
            "message": "Метод оплаты успешно обновлен",
            "method": self._public(db_method_payment_update)
        }
         
    def Sdelete_method_payment(self, метод: Optional[str], метод_id: Optional[int]) -> Dict[str, Any]:
        self.repository.delete_method(метод, метод_id)

        return {
            "message": "Метод оплаты успешно удален"
        }