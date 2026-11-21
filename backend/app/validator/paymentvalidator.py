from typing import Dict, Any, List, Optional
from decimal import Decimal
from fastapi import HTTPException
from datetime import date, datetime 
from ..repositories import Cprepository

class Cpaymnetvalidator:
    def __init__(self, repository: Cprepository):
        self.repository = repository

    def validate_create_payment(self, paymentdata: Dict[str, Any]):

        required_fields = ["заказы", "цена", "метод", "статус", "дата"] 

        for field in required_fields: 

            if field not in paymentdata or not paymentdata[field]: 

                raise HTTPException(status_code=400, detail=f"Поле '{field}' обязательно для заполнения")

        parsed_data = paymentdata.copy()

        if isinstance(parsed_data["дата"], str):
            try:
                parsed_data["дата"] = datetime.strptime(parsed_data["дата"], "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="неверный формат даты")
    
        price = Decimal(str(parsed_data["цена"]))

        if price < 0:
            raise HTTPException(status_code=400, detail="Цена не может быть отрицательной")

        if not self.repository.get_order_by_id(заказы=parsed_data["заказы"]):
            raise HTTPException(status_code=404, detail="Такого заказа не существует")
        
        if not self.repository.get_method_by_id(метод=parsed_data["метод"]):
            raise HTTPException(status_code=404, detail="Указанный метод оплаты не существует")

        if not self.repository.get_status_by_id(статус=parsed_data["статус"]):
            raise HTTPException(status_code=404, detail="Указанный статус не существует")


        existing_payment = self.repository.duplicate_payment(цена=parsed_data["цена"], метод=parsed_data["метод"], заказы=parsed_data["заказы"])

        if existing_payment:
            raise HTTPException(status_code=400, detail="Такой заказ уже существует")

        return parsed_data
        
    
    def validate_update_payment(self, updatepaymentdata: Dict[str, Any]):

        parsed_data = updatepaymentdata.copy()

        if "дата" in parsed_data and isinstance(parsed_data["дата"], str):
            try:
                parsed_data["дата"] = datetime.strptime(parsed_data["дата"], "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="неверный формат даты")