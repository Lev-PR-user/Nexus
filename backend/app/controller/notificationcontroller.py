from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Cnotificationservice, require_roles

ANRoute = APIRouter(
    prefix="/notifications",
    tags=["/notifications"],
    dependencies=[Depends(require_roles(["админ"]))]
)

@ANRoute.get("/notifications")
def get_all(db: Session = Depends(get_db)):
    try:
        service = Cnotificationservice(db)
        return service.Sget_all()
    except HTTPException: raise
    except Exception as e: raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")

@ANRoute.get("/notification_search")
def get_by_id(уведомление_id: int, db: Session = Depends(get_db)):
    try:
        service = Cnotificationservice(db)
        return service.Sget_notification(уведомление_id)
    except HTTPException: raise
    except Exception as e: raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")

@ANRoute.get("/notifications_by_user")
def get_by_user(пользователь_id: int, db: Session = Depends(get_db)):
    try:
        service = Cnotificationservice(db)
        return service.Sget_by_user(пользователь_id)
    except HTTPException: raise
    except Exception as e: raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")

@ANRoute.post("/notification_create")
def create_notification(notificationdata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Cnotificationservice(db)
        return service.create_notification(notificationdata)
    except HTTPException: raise
    except Exception as e: raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")

@ANRoute.delete("/notification_delete")
def delete_notification(уведомление_id: int, db: Session = Depends(get_db)):
    try:
        service = Cnotificationservice(db)
        return service.Sdelete_notification(уведомление_id)
    except HTTPException: raise
    except Exception as e: raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")