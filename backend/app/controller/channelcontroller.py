from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Cchannelnotificationservice, require_roles

ACNRoute = APIRouter(
    prefix="/channel_notification", 
    tags=["/channel_notification"],
    dependencies=[Depends(require_roles(["админ"]))]
    )

@ACNRoute.get("/get_all_channe")
def get(db: Session = Depends(get_db)):
    try:
        service = Cchannelnotificationservice(db)
        return service.get_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении канала уведомления: {str(e)}")

@ACNRoute.post("/create_channe_notification")
def create_category_notification(chndata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Cchannelnotificationservice(db)
        return service.Screate_channel(chndata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании канала уведомления: {str(e)}")

@ACNRoute.put("/update_channe_notification")
def update_category_notification(канал_уведомления_id: int, updatechndata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Cchannelnotificationservice(db)
        return service.Supdate_channel(канал_уведомления_id, updatechndata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении канала уведомления: {str(e)}")

@ACNRoute.delete("/delete_channe_notification")
def delete_category_notification(канал_уведомления_id: int, db: Session = Depends(get_db)):
    try:
        service = Cchannelnotificationservice(db)
        return service.Sdelete_channel(канал_уведомления_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении канала уведомления: {str(e)}")