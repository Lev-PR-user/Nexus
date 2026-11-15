from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import Date
from ..db import get_db
from ..services import Cpservice, require_roles, get_current_user

AMPYRouter = APIRouter(
    prefix="payments_methods", 
    tags=["payments_methods"],
    dependencies=[Depends(require_roles(["админ"]))]
    )

MMPRouter = APIRouter(
    prefix="payments_methods", 
    tags=["payments_methods"],
    dependencies=[Depends(require_roles(["админ", "менеджер"]))]
)

@MPAYRouter.get("/methods")
def get_all(db: Session = Depends(get_db)):
    try:
        service = Cpservice(db)
        return service.Sget_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении метода платежа: {str(e)}")

@MPAYRouter.get("/method_search")
def search(метод: Optional[str], метод_id: Optional[int], db: Session = Depends(get_db)):
    try:
        service = Cpservice(db)
        return service.Ssearch(метод, метод_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении метода платежа: {str(e)}")

@APAYRouter.post("/method_create")
def create_method(methodpaymentdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Cpservice(db)
        return service.Screate_method_payment(methodpaymentdata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании метода платежа: {str(e)}")

@APAYRouter.put("/method_update")
def update_method(updatemethodpaymentdata: Dict[str, Any], метод: Optional[str] = None, метод_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        service = Cpservice(db)
        return service.Supdate_method_payment(updatemethodpaymentdata, метод, метод_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении метода платежа: {str(e)}")

@APAYRouter.delete("method_delete")
def delete_method(метод: Optional[str] = None, метод_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        service = Cpservice(db)
        return service.Sdelete_method_payment(метод, метод_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении метода платежа: {str(e)}")