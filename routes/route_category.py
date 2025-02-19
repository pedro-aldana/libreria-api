from fastapi import APIRouter,HTTPException,Depends
from models.model_category import Category
from schemas.schema_category import CategoryCreate,CategoryUpdate,CategoryOut
from auth.auth import get_current_user
from crud.crud_category import create_category, get_categories,get_category_by_id, update_category, delete_category
from utils.dependencies import is_admin_or_superadmin


category_router  = APIRouter()


@category_router.post("/create/", response_model=CategoryOut, dependencies=[Depends(is_admin_or_superadmin)])
async def create_category_enpoint(category: CategoryCreate):
    return await create_category(category.name.strip())


@category_router.get("/list/", response_model=list[CategoryOut])
async def get_categories_enpoint():
    return await get_categories()


@category_router.get("/by_id/{category_id}", response_model=CategoryOut)
async def get_category_enpoint(category_id: int):
    return await get_category_by_id(category_id)


@category_router.patch("/update/{category_id}", response_model=CategoryOut, dependencies=[Depends(is_admin_or_superadmin)])
async def update_category_enpoint(category_id: int, category: CategoryUpdate):
    return await update_category(category_id, category.new_name)

@category_router.delete("/delete/{category_id}", dependencies=[Depends(is_admin_or_superadmin)])
async def delete_category_enpoint(category_id: int):
    return await delete_category(category_id)
