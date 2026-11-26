from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import Ccategorynotificationservice, require_roles

ACANRoute = APIRouter(
    prefix="/categories_notification", 
    tags=["/categories_notification"],
    dependencies=[Depends(require_roles(["админ"]))]
    )

@ACANRoute.get("/get_all_category")
def get(db: Session = Depends(get_db)):
    try:
        service = Ccategorynotificationservice(db)
        return service.get_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении категории уведомления: {str(e)}")

@ACANRoute.post("/create_category_notification")
def create_category_notification(categorynotificationata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Ccategorynotificationservice(db)
        return service.create_category_notification(categorynotificationata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании категории уведомления: {str(e)}")

@ACANRoute.put("/update_category_notification")
def update_category_notification(категория_уведомления_id: int, updatecategorynotificationata: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        service = Ccategorynotificationservice(db)
        return service.update_category_notfication(категория_уведомления_id, updatecategorynotificationata)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении категории уведомления: {str(e)}")

@ACANRoute.delete("/delete_category_notification")
def delete_category_notification(категория_уведомления_id: int, db: Session = Depends(get_db)):
    try:
        service = Ccategorynotificationservice(db)
        return service.delete_category_notification(категория_уведомления_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении категории уведомления: {str(e)}")