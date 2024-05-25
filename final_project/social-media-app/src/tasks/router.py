from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
    
from auth.di import get_current_user as current_user

from .tasks import send_email_report_dashboard
from sqlalchemy.orm import Session
from database import get_db
from auth.service import get_current_user

router = APIRouter(prefix="/report")


@router.get("/dashboard")
async def get_dashboard_report(background_tasks: BackgroundTasks, token: str, db: Session = Depends(get_db)):
    db_user = await get_current_user(db, token)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
        )
   
    if not db_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # 1400 ms - Client waits
    # send_email_report_dashboard(user.username)
    # 500 ms - Task runs in the background of FastAPI in the event loop or another thread
    # background_tasks.add_task(send_email_report_dashboard, user.username)
    # 600 ms - Task runs in a separate process by the Celery worker
    send_email_report_dashboard.delay(db_user.username)
    return {
        "status": 200,
        "data": "Email sent",
        "details": None
    }
    