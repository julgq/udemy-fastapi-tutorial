from fastapi import FastAPI, HTTPException, Request, status, Form, Header
# pydantic para la creación de modelos y validación automática de datos.
# Filed para requerir una validación especifica del campo.
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

# Json response personalizado.
from starlette.responses import JSONResponse


# https://fastapi.tiangolo.com/tutorial/handling-errors/

class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return

app = FastAPI()

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the book", max_length=100, min_length=1)
    rating: int = Field(gt=-1, lt=101) 

    # class config ayuda a definir un ejemplo de request para el /docs
    class Config:
        schema_extra = {
            "example": {
                "id": "458d0835-4655-4fdb-b6bf-fc1d85045ae3",
                "title": "Computer Since",
                "author": "Corporation",
                "description": "A very nice description of a book",
                "rating": 1
            }
        }

# BookNoRating, un modelo sin el rating, esto ayuda a decorar el response .
class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(
        None, title="description of the Book", 
        max_length=1000, 
        min_length=1
    )


BOOKS = []

# manejador de excepciones personalizado
@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request, exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Hey, Why do you want {exception.books_to_return} books? you need to read more!"}
    )

# Form, tipicamente usado cuando se envian valores desde un formulario.
# application/x-www-form-urlencoded
@app.post("/books/login")
async def book_login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}

# Header, para enviar valores de header.
@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header": random_header}

@app.get("/")
# books_to_return es un query parameter opcional
def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

    if len(BOOKS) < 1:
        create_books_no_api()
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS

@app.get("/book/{book_id}")
async def reed_book(book_id:UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x


    
# En este modelo se decora la salida.
@app.get("/book/ratinng/{book_id}", response_model=BookNoRating)
async def reed_book_no_reating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter -1] = book
            return BOOKS[counter -1]
    raise raise_item_cannot_be_found_exception()

@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter -1]
            return f'ID:{book_id} deleted'
    
    # crear una excepción 
    raise raise_item_cannot_be_found_exception()


def create_books_no_api():
    book_1 = Book(id="458d0835-4655-4fdb-b6bf-fc1d85045ae3", title="string", author="string", description="string", rating=2)
    BOOKS.append(book_1)
    book_2 = Book(id="458d0835-4655-4fdb-b6bf-fc1d85045ae3", title="string", author="string", description="string", rating=2)
    BOOKS.append(book_2)


def raise_item_cannot_be_found_exception():
    return  HTTPException(status_code=404, detail="Book not found", headers={'X-Header-Error': "Nothing to be ssen at the UUID"})