from typing import Dict, Any, Optional
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db 
from ..services import require_roles, Cspservice

ASPRouter = APIRouter(prefix="/status_payment", 
                    tags=["/status_payment"],
                    dependencies=[Depends(require_roles(["админ"]))]
                    )


MSPRouter = APIRouter(prefix="/status_payment", 
                    tags=["/status_payment"],
                    dependencies=[Depends(require_roles(["админ", "менеджер"]))]
                    )

@MSPRouter.get("/statuses")
def get_all(db: Session = Depends(get_db)):
    try:
        service = Cspservice(db)
        return service.Sget_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении статуса платежа: {str(e)}")
    
@MSPRouter.get("/status_search")
def search(статусы_оплаты_id: Optional[int] = None, название: Optional[str] = None,  db: Session = Depends(get_db)):
    try:
        service = Cspservice(db)
        return service.Ssearch(статусы_оплаты_id, название)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении статуса платежа: {str(e)}")

@ASPRouter.post("/status_create")
def create_status(statuspaymentdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Cspservice(db)
        return service.Screate_status(statuspaymentdata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании статуса платежа: {str(e)}")

@ASPRouter.put("/update_status")
def update_status(updatestatuspaymentdata: Dict[str, Any], статусы_оплаты_id: Optional[int] = None, название: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        service = Cspservice(db)
        return service.Supdate_status(updatestatuspaymentdata, статусы_оплаты_id, название)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении статуса платежа: {str(e)}")

@ASPRouter.delete("/status_delete")
def delete_status(статусы_оплаты_id: Optional[int] = None, название: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        service = Cspservice(db)
        return service.Sdelete_status(статусы_оплаты_id, название)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении статуса платежа: {str(e)}")