from models.model_user import Role,User
from schemas.schema_role import RoleCreate
from fastapi import HTTPException


async def create_role(name:str, description: str | None = None):
    existing_role = await Role.get_or_none(name=name)
    if existing_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    
    role = await Role.create(name=name, description=description)
    return role

async def get_roles():
    return await Role.all()

async def get_role_by_id(role_id: int):
    role = await Role.get_or_none(id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

async def assing_role_to_user(user_id: int, role_id: int):
    user = await User.get_or_none(id=user_id)
    role = await Role.get_or_none(id=role_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    user.role = role
    await user.save()
    return user


async def delete_role(role_id: int):
    role = await get_role_by_id(role_id)
    await role.delete()
    return role