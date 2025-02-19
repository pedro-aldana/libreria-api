from models.model_user import User, Role
from passlib.context import CryptContext
from fastapi import HTTPException,status
from auth.auth import verify_password,create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(email: str, password: str, username: str):
    user_role = await Role.get_or_none(name="user")
    if not user_role:
        user_role = await Role.create(name="user", description="Default user role")
    
    hashed_password = pwd_context.hash(password)
    user = await User.create(
        email=email,
        password=hashed_password,
        username=username,
        role=user_role
    )
    return user



async def get_users():
    users= await User.all().prefetch_related("role")
    return users

async def get_user_by_email(email: str):
    user = await User.get_or_none(email=email)
    return user

async def update_user(email: str, new_username: str, new_password: str, new_role_id: int,new_profile_img: str,new_banner_img: str):
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if new_username:
        user.username = new_username
    if new_password:
        user.password = pwd_context.hash(new_password)
    if new_role_id:
        role = await Role.get_or_none(id=new_role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        user.role = role

    if new_profile_img:
        user.profile_img = new_profile_img
    if new_banner_img:
        user.banner_img = new_banner_img        

        

    await user.save()
    return user

async def delete_user(email: str):
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user.delete()

async def verify_user(form_data):
    user = await User.get_or_none(email=form_data.username)

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token":access_token, "token_type": "bearer"}
    
