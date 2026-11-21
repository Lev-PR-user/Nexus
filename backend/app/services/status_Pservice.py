from typing import Dict, Any, Optional
from fastapi import HTTPException
from ..repositories import Csprepository
# from ..validator import 

class Cspservice():
    def __init__(self, db):
        self.db = db
        self.repository = Csprepository(db)

    @staticmethod
    def _public(db_status_payment):
        return {
            "id": db_status_payment.статусы_оплаты_id,
            "name": db_status_payment.название
        }  
    
    def Sget_all(self):
        return [self._public(sp) for sp in self.repository.get_all()] 

    def Ssearch(self, статусы_оплаты_id: Optional[int], название: Optional[str]) -> Dict[str, Any]:
        if название:
            db_status_payment = self.repository.status_by_name(название)
        elif статусы_оплаты_id:
            db_status_payment = self.repository.status_by_id(статусы_оплаты_id)
        else:
            raise HTTPException(status_code=400, detail="Введите данные для поиска")

        if db_status_payment is None:
            raise HTTPException(status_code=400, detail="Статус оплаты не найден") 

        return self._public(db_status_payment)

    def Screate_status(self, statuspaymentdata: Dict[str, Any]):
        
        db_status_payment_data = {
            "name": statuspaymentdata["название"]
        }

        db_status_payment = self.repository.create_status(db_status_payment_data)

        return {
            "message": "Статус оплаты создан успешно",
            "status_payment": self._public(db_status_payment)
        }

    def Supdate_status(self, updatestatuspaymentdata: Dict[str, Any], статусы_оплаты_id: Optional[int], название: Optional[str]) -> Dict[str, Any]:
        db_status_payment_update_data = {}

        if "название" in updatestatuspaymentdata:
            db_status_payment_update_data["name"] = updatestatuspaymentdata["название"]

        db_status_payment_update = self.repository.update_status(db_status_payment_update_data, статусы_оплаты_id, название)

        return {
            "message": "Статус оплаты успешно обновлен",
            "status_payment": self._public(db_status_payment_update)
        }

    def Sdelete_status(self, статусы_оплаты_id: Optional[int], название: Optional[str]) -> Dict[str, Any]:

        self.repository.delete_status(статусы_оплаты_id, название)

        return {
            "message": "Статус опоаты успешно удален"
        }