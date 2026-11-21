from typing import Dict, Any, Optional, List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import СтатусыОплатыM

class Csprepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[СтатусыОплатыM]:
        try:
            return self.db.query(СтатусыОплатыM).all()
        except HTTPException:
            self.db.rollback()
            raise

    def status_by_id(self, статусы_оплаты_id: Optional[int]) -> Optional[СтатусыОплатыM]:
        try: 
            if статусы_оплаты_id is None:
                return None
            return self.db.query(СтатусыОплатыM).filter(СтатусыОплатыM.статусы_оплаты_id == статусы_оплаты_id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")

    def status_by_name(self, название: Optional[str]) -> Optional[СтатусыОплатыM]:
        try: 
            if название is None: 
                return None
            return self.db.query(СтатусыОплатыM).filter(СтатусыОплатыM.название == название).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка в базе данных: {str(e)}")

    def create_status(self, statuspaymentdata: Dict[str, Any]) -> Optional[СтатусыОплатыM]:
        try: 
            status_pyment_db = СтатусыОплатыM(
                название=statuspaymentdata["name"]
            )

            self.db.add(status_pyment_db)

            self.db.commit()

            self.db.refresh(status_pyment_db)

            return status_pyment_db
        except HTTPException:
            self.db.rollback()
            raise
    
    def update_status(self, updatestatuspaymentdata: Dict[str, Any], статусы_оплаты_id: Optional[int], название: Optional[str]) -> Optional[СтатусыОплатыM]:
        try: 
            update_status_pyment_db = self.status_by_id(статусы_оплаты_id) or self.status_by_name(название)
             
            if update_status_pyment_db is None:
                raise HTTPException(status_code=500, detail="Такая статус оплаты не найден")
            
            if "name" in updatestatuspaymentdata:
                update_status_pyment_db.название = updatestatuspaymentdata["name"]

            self.db.commit()

            self.db.refresh(update_status_pyment_db)

        except HTTPException:
            self.db.rollback()
            raise

    def delete_status(self, статусы_оплаты_id: Optional[int], название: Optional[str]) -> bool:
        try:
    
            status_pyment_db = self.status_by_id(статусы_оплаты_id) or self.status_by_name(название)

            if status_pyment_db is None:
                return False

            self.db.delete(status_pyment_db)

            self.db.commit()

            return True
        
        except HTTPException:
            self.db.rollback()
            raise