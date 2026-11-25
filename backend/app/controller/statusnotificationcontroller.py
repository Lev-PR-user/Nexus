from typing import Dict, Any
from ..services import Cstatusnotification, require_roles
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, APIRouter
from ..db import get_db

ASNRouter = APIRouter(
    prefix="/status_notifications",
    tags=["/status_notifications"],
    dependencies=[Depends(require_roles(["админ"]))]
    )

@ASNRouter.post("/create_status_notifications")
def status_notification_create(notificationdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Cstatusnotification
        return service.Screate_notification(notificationdata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании статуса уведомления: {str(e)}")

@ASNRouter.put("/update_status_notifications")
def status_notifications_update(статус_оборудования_id: int, updatenotificationdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Cstatusnotification(db)
        return service.Supdate_status_notification(статус_оборудования_id, updatenotificationdata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении статуса уведомления: {str(e)}")

@ASNRouter.delete("delete_status_notification")
def status_notification_delete(статус_оборудования_id: int, db: Session = Depends(get_db)):
    try:
        service = Cstatusnotification(db)
        return service.Sdelete_status_notification(статус_оборудования_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении статуса уведомления: {str(e)}")