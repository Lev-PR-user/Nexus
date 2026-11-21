from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import HTTPException

class Cordervalidator():
    def create_order(self, orderdata: Dict[str, Any]):

        required_fields = ["услуги", "локации", "дата_начала", "дата_конца"]

        for field in required_fields:
            if field not in orderdata or not orderdata[field]:
                raise HTTPException(status_code=400, detail=f"Поля '{field}' обязательно для заполнения")
            
        parsed_data = orderdata.copy()

        if isinstance(parsed_data["дата_начала"], str):
            try:
                parsed_data["дата_начала"] = datetime.strptime(parsed_data["дата_начала"], "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="неверный формат даты")
            
        if isinstance(parsed_data["дата_конца"], str):
            try:
                parsed_data["дата_конца"] = datetime.strptime(parsed_data["дата_конца"], "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="неверный формат даты")
            
        return parsed_data

    def assign_resources(self, orderdata: Dict[str, Any]):

        required_fields = ["оператор", "оборудование"]

        for field in required_fields:
            if field not in orderdata or not orderdata[field]:
                raise HTTPException(status_code=400, detail=f"Поля '{field}' обязательно для заполнения")