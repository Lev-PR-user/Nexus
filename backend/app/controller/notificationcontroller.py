from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Cnotificationservice, require_roles

NRoute = APIRouter(
    prefix="/notifications",
    tags=["/notifications"],
    dependencies=[Depends(require_roles(["админ"]))]
)

@NRoute.get("/notifications")
def get_all(db: Session = Depends(get_db)):
    try:
        service = Cnotificationservice(db)
        return service.Sget_all()
    except HTTPException: raise
    except Exception as e: raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")

@NRoute.get("/notification_search")
def get_by_id(уведомление_id: int, db: Session = Depends(get_db)):
    try:
        service = Cnotificationservice(db)
        return service).Sget_notification(уведомление_id)
    except HTTPException: raise
    except Exception as e: raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")

@NRoute.get("/notifications_by_user")
def get_by_user(пользователь_id: int, db: Session = Depends(get_db)):
    try:
        service = Cnogittificationservice(db)
        return service.Sget_by_user(пользователь_id)
    except HTTPException: raise
    except Exception as e: raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")

@NRoute.post("/notification_create")
def create_notification(data: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Cnotificationservice(db)
        return service.Screate_notification(data)
    except HTTPException: raise
    except Exception as e: raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")

@NRoute.delete("/notification_delete")
def delete_notification(уведомление_id: int, db: Session = Depends(get_db)):
    try:
        service = Cnotificationservice(db)
        return service.Sdelete_notification(уведомление_id)
    except HTTPException: raise
    except Exception as e: raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")