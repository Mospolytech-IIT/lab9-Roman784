'''main.py'''


from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Depends
import uvicorn
from database import create_tables, delete_tables
from repository import User, Post, UserRepository, PostRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


# CRUD для работы с пользователем
@app.post("/create-user")
async def create_user(user: Annotated[User, Depends()]):
    '''Создаёт пользователя'''
    user_id = await UserRepository.add_one(data=user)
    return {"id": user_id}

@app.get("/get-all-users")
async def get_all_users():
    '''Возвращает всех пользователей'''
    users = await UserRepository.get_all()
    return users

@app.put("/update-user-email")
async def update_user_email(user_id: int, new_email: str):
    '''Обновляет данные пользователя'''
    await UserRepository.update_email(user_id=user_id, new_email=new_email)

@app.delete("/delete-user")
async def delete(user_id: int):
    '''Удаляет пользоватлея вместе с его постами'''
    await UserRepository.delete(user_id=user_id)


# CRUD для работы с постами
@app.post("/create-post")
async def create_post(post: Annotated[Post, Depends()]):
    '''Создаёт пост'''
    post_id = await PostRepository.add_one(data=post)
    return {"id": post_id}

@app.get("/get-all-posts")
async def get_all_posts():
    '''Возвращает все посты'''
    posts = await PostRepository.get_all()
    return posts

@app.get("/get-posts")
async def get_posts(user_id: int):
    '''Возвращает все посты конкретного пользователя'''
    posts = await PostRepository.get_posts(user_id=user_id)
    return posts

@app.put("/update-post-content")
async def update_post_content(post_id: int, new_content: str):
    '''Обновляет content поста'''
    await PostRepository.update_content(post_id=post_id, new_content=new_content)

@app.delete("/delete-post")
async def delete_post(post_id: int):
    '''Удаляет пост'''
    await PostRepository.delete(post_id=post_id)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
