from fastapi import APIRouter,Depends
from models.model_book import Book
from schemas.schema_book import BookCreate,BookOut,BookUpdate
from crud.crud_book import create_book,get_books,get_book_by_id,get_books_by_category,get_books_by_user,update_book,delete_book
from auth.auth import get_current_user
from typing import List
from tortoise.expressions import Q

book_router = APIRouter()

@book_router.post("/create/", response_model=BookOut)
async def create_book_endpoint(book: BookCreate, user=Depends(get_current_user)):
    created_book = await create_book(
        book.title, 
        book.author, 
        book.description, 
        book.cover_image, 
        book.category_id, 
        user.id,
        book.archive,
        book.rating
    )

    # Retornar el libro creado, ya con las relaciones cargadas
    return created_book



@book_router.get("/list/", response_model=List[BookOut])
async def get_books_endpoint():
    return await get_books()

@book_router.get("/by_id/{book_id}",response_model=BookOut)
async def get_book_by_id_endpoint(book_id: int):
    return await get_book_by_id(book_id)

@book_router.get("/category/{category_id}", response_model=List[BookOut])
async def get_books_by_category_endpoint(category_id: int):
    return await get_books_by_category(category_id)


@book_router.get("/search/")
async def search_books_endpoint(query: str = ""):
    books = await Book.filter(Q(title__icontains=query)|Q(author__icontains=query))
    return [{"id": book.id, "title": book.title, "author": book.author, "cover_image": book.cover_image} for book in books]

@book_router.get("/my-books/", response_model=List[BookOut])
async def get_my_books_endpoint(user=Depends(get_current_user)):
    return await get_books_by_user(user.id)

@book_router.patch("/by_id/{book_id}", response_model=BookOut)
async def update_book_endpoint(book_id:int, book: BookUpdate, user=Depends(get_current_user)):
    return await update_book(book_id,book,user_id=user.id)

@book_router.delete("/by_id/{book_id}")
async def delete_book_endpoint(book_id: int, user=Depends(get_current_user)):
    return await delete_book(book_id, user_id=user.id)