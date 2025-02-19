from fastapi import APIRouter, Depends, HTTPException
from schemas.schema_user import UserCreate, UserOut, UserUpdate, UserLogin, Token
from models.model_user import User
from crud.crud_user import create_user, update_user, delete_user, get_user_by_email, verify_user,get_users
from fastapi.security import OAuth2PasswordRequestForm
from auth.auth import get_current_user
from typing import List
from utils.dependencies import is_superadmin

user_router = APIRouter()

@user_router.post("/users/", response_model=UserOut)
async def create_user_endpoint(user: UserCreate):
    return await create_user(user.email, user.password, user.username)


@user_router.get("/users/list/", response_model=List[UserOut],dependencies=[Depends(is_superadmin)])
async def get_users_enpoint():
    return await get_users()

@user_router.get("/users/{email}", response_model=UserOut)
async def get_user_endpoint(email: str):
    user = await get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.get("/users/", response_model=UserOut)
async def get_me_endpoint(current_user: User = Depends(get_current_user)):
    return current_user

@user_router.patch("/users/{email}", response_model=UserOut)
async def update_user_endpoint(email: str, user: UserUpdate, current_user: User = Depends(get_current_user)):
    # Solo permite el cambio de rol si el usuario es admin
    if current_user.role.name != "superadmin" and current_user.email != email:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return await update_user(email, user.new_username, user.new_password, user.new_role_id, user.new_profile_img, user.new_banner_img)

@user_router.delete("/users/{email}")
async def delete_user_endpoint(email: str, current_user: User = Depends(get_current_user)):
    if current_user.role.name != "superadmin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return await delete_user(email)

@user_router.post("/login/", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    return await verify_user(form_data)
