from fastapi import APIRouter, Depends
from fastapi_azure_auth.user import User

from app.core.config import settings
from app.core.security import get_bearer_token, get_current_user

router = APIRouter(
    prefix="/api/health",
    tags=["health"],
)

@router.get("/")
async def health():
    print(settings.entra_audience)
    return {"message": "ok"}

@router.get("/token")
async def IsToken(token: str = Depends(get_bearer_token)) -> dict:
    return {
        "auth":True
    }

@router.get("/user")
async def get_user(user: User = Depends(get_current_user)) -> dict:
    return user.model_dump()