from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import Date
from ..db import get_db
from ..services import Cpmservice, require_roles, get_current_user

APAYRouter = APIRouter(
    prefix="payments", 
    tags=["payments"],
    dependencies=[Depends(require_roles(["админ"]))]
    )

MPAYRouter = APIRouter(
    prefix="payments", 
    tags=["payments"],
    dependencies=[Depends(require_roles(["админ", "менеджер"]))]
)

@MPAYRouter.get("/payments")
def get_all(db: Session = Depends(get_db)):
    try:
        service = Cpmservice(db)
        return service.Sget_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении платежа: {str(e)}")

@MPAYRouter.get("/search")
def search(платежи_id: Optional[int] = None, заказы_id: Optional[int] = None, статус_id: Optional[int] = None, метод_id: Optional[int] = None, дата_от: Optional[Date] = None, дата_до: Optional[Date] = None, db: Session = Depends(get_db)):
    try:
        service = Cpmservice(db)
        return service.Ssearch(платежи_id, заказы_id, статус_id, метод_id, дата_от, дата_до)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении платежа: {str(e)}")

@APAYRouter.post("/payment_create")
def create_payment(paymentdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Cpmservice(db)
        return service.Screte_payment(paymentdata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании платежа: {str(e)}")

@APAYRouter.put("/payment_update")
def update_payment(платежи_id: int, updatepaymentdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Cpmservice(db)
        return service.Supdate_payment(платежи_id, updatepaymentdata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении платежа: {str(e)}")

@APAYRouter.delete("payment_delete")
def delete_payment(платежи_id: int, db: Session = Depends(get_db)):
    try:
        service = Cpmservice(db)
        return service.Sdelete_payment(платежи_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении платежа: {str(e)}")