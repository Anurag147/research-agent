from fastapi import Depends, HTTPException
from fastapi.params import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer
from fastapi_azure_auth.user import User

from app.core.config import settings

bearer_scheme = HTTPBearer()
azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=settings.entra_client_id,
    tenant_id=settings.entra_tenant_id,
    allow_guest_users=True,
)


async def get_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Bearer token required")
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Bearer token required")
    return token


async def get_current_user(
    user: User = Security(azure_scheme, scopes=["research.read"]),
):
    if not user:
        raise HTTPException(status_code=401, detail="Bearer token required")
    return user
