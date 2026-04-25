from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    data = service.login(payload.username, payload.password)
    return TokenResponse(access_token=data["access_token"], role=data["role"], username=data["username"])

