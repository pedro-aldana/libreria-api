from models.model_category import Category
from fastapi import HTTPException, status
from tortoise.exceptions import IntegrityError,DoesNotExist

async def create_category(name: str) -> Category:
    """Crea una nueva categoría."""
    try:
        category = await Category.create(name=name)
        return category
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists",
        )

async def get_categories() -> list:
    return await Category.all()


async def get_category_by_id(category_id: int) -> Category:
    try:
        category = await Category.get(id=category_id)
        return category
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

async def update_category(category_id: int, new_name: str) -> Category:
    category = await get_category_by_id(category_id)
    if new_name:
        category.name = new_name

    await category.save()
    return category

async def delete_category(category_id: int) -> Category:
    category = await get_category_by_id(category_id)
    await category.delete()
    return category  

