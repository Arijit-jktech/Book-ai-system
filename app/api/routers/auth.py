from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, hash_password, verify_password
from app.schemas.user import Token

router = APIRouter(prefix="/auth", tags=["auth"])

users_db = {
    "admin": {"username": "admin", "password_hash": hash_password("adminpass"), "role": "admin"},
    "alice": {"username": "alice", "password_hash": hash_password("alicepass"), "role": "user"}
}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token({"username": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}
