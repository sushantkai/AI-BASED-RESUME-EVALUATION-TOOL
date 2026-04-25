from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_roles
from app.schemas.dashboard_schema import DashboardResponse
from app.services.dashboard_service import DashboardService


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse, dependencies=[Depends(require_roles("Admin", "HR"))])
def get_dashboard(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return DashboardService(db).get_dashboard_data()

