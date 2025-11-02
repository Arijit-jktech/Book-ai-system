from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token
from app.schemas.user import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    payload = decode_token(token)
    if not payload or "username" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth credentials")
    return TokenData(username=payload.get("username"), role=payload.get("role"))

def require_role(role: str):
    async def _require_role(user = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Insufficient privileges")
        return user
    return _require_role
