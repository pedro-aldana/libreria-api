from fastapi import APIRouter, Depends
from models.model_user import User
from schemas.schema_role import RoleCreate,RoleOut,RoleAssing
from crud.crud_role import create_role,get_roles,get_role_by_id,assing_role_to_user,delete_role
from utils.dependencies import is_superadmin


role_router = APIRouter()

@role_router.post("/roles/", response_model=RoleOut, dependencies=[Depends(is_superadmin)])
async def create_role_endpoint(role: RoleCreate):
    return await create_role(role.name,role.description)

@role_router.get("/roles/", response_model=list[RoleOut])
async def get_roles_endpoint():
    return await get_roles()

@role_router.get("/roles/{role_id}", response_model=RoleOut)
async def get_role_by_id_endpoint(role_id: int):
    return await get_role_by_id(role_id)

@role_router.post("/roles/assign/")
async def assign_role_to_user_endpoint(role_data: RoleAssing, user: User = Depends(is_superadmin)):
    return await assing_role_to_user(role_data.user_id,role_data.role_id)

@role_router.delete("/roles/{role_id}", dependencies=[Depends(is_superadmin)])
async def delete_role_enpoint(role_id:int):
    return await delete_role(role_id)     