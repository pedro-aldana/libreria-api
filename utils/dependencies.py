from fastapi import Depends,HTTPException
from models.model_user import Role,User
from auth.auth import get_current_user

async def is_superadmin(user: User = Depends(get_current_user)):
    if not user.role or user.role.name != "superadmin":
        raise HTTPException(status_code=403, detail="Access forbidden: Only superadmins can perform this action")
    return user

async def is_admin_or_superadmin(user: User = Depends(get_current_user)):
    if not user.role or user.role.name not in ["admin","superadmin"]:
        raise HTTPException(status_code=403, detail="Access forbidden: Only admins and superadmins can perform this action")
    return user