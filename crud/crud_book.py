from models.model_book import Book
from models.model_category import Category
from models.model_user import User
from schemas.schema_book import BookUpdate
from tortoise.exceptions import DoesNotExist
from fastapi import HTTPException, status
from tortoise.transactions import in_transaction

async def create_book(
    title: str, author: str, description: str, cover_image: str, category_id: int, user_id: int, archive: str,rating: int
):
   async with in_transaction() as conn:
        # Crear el libro con los valores explícitos para los campos
        book_obj = await Book.create(
            title=title.strip(),
            author=author.strip(),
            description=description.strip(),
            cover_image=cover_image.strip(),
            category_id=category_id,
            user_id=user_id,
            archive=archive.strip(),
            rating=rating
        )
   return book_obj



async def get_books():
    books = await Book.all().prefetch_related("user","category").values(
        "id", "title", "author", "description", "cover_image","rating","archive", "created_at",
        "user__id", "user__username", "user__email",
        "category__id", "category__name"
    )

    formatted_books = [
        {
            "id": book["id"],
            "title": book["title"],
            "author": book["author"],
            "description": book["description"],
            "cover_image": book["cover_image"],
            "rating": book["rating"],
            "archive": book["archive"],
            "created_at": book["created_at"],
            "user": {
                "id": book["user__id"],
                "username": book["user__username"],
                "email": book["user__email"],
            },
            "category": {
                "id": book["category__id"],
                "name": book["category__name"],
            },
        }
        for book in books
    ]

    return formatted_books

async def get_book_by_id(book_id: int):
    try:
        # Usamos select_related para obtener las relaciones de 'user' y 'category'
        book = await Book.filter(id=book_id).select_related("user", "category").first()

        # Verificamos si el libro fue encontrado
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

        # Formateamos el libro con sus relaciones
        formatted_book = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "description": book.description,
            "cover_image": book.cover_image,
            "rating": book.rating,
            "archive": book.archive,
            "created_at": book.created_at,
            "user": {
                "id": book.user.id,
                "username": book.user.username,
                "email": book.user.email,
            },
            "category": {
                "id": book.category.id,
                "name": book.category.name,
            },
        }

        return formatted_book
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")



async def get_books_by_category(category_id: int):
    return await Book.filter(category_id=category_id).prefetch_related("user","category")

async def get_books_by_user(user_id: int):
    books = await Book.filter(user_id=user_id).prefetch_related("category", "user").values(
        "id",
        "title",
        "author",
        "description",
        "cover_image",
        "rating",
        "archive",
        "created_at",
        "category__id",  # Campos de la categoría
        "category__name",
        "user__id",       # Campos del usuario
        "user__username",
        "user__email",
    )
    return [
        {
            "id": book["id"],
            "title": book["title"],
            "author": book["author"],
            "description": book["description"],
            "cover_image": book["cover_image"],
            "rating": book["rating"],
            "archive": book["archive"],
            "created_at": book["created_at"],
            "category": {
                "id": book["category__id"],
                "name": book["category__name"],
            },
            "user": {
                "id": book["user__id"],
                "username": book["user__username"],
                "email": book["user__email"],
            },
        }
        for book in books
    ]   


async def update_book(book_id: int, book: BookUpdate, user_id: int):
    # Obtener el libro filtrado por id y user_id
    book_obj = await Book.filter(id=book_id, user_id=user_id).first()  # Utilizamos .first() para obtener el primer resultado o None
    
    if not book_obj:
        raise HTTPException(status_code=404, detail="Libro no encontrado o no eres el dueño de este libro")

    # Actualizar los campos del libro
    if book.title:
        book_obj.title = book.title
    if book.description:
        book_obj.description = book.description
    if book.author:
        book_obj.author = book.author
    if book.category_id:
        book_obj.category_id = book.category_id
    if book.cover_image:
        book_obj.cover_image = book.cover_image

    # Guardar los cambios
    await book_obj.save()
    return book_obj


async def delete_book(book_id: int, user_id: int):
    book = await Book.filter(id=book_id, user_id=user_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    await book.delete()
    return {"message": "Libro eliminado correctamente"}