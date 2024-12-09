'''Функции для работы с бд'''


from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from pydantic import BaseModel
from database import new_session, UserTable, PostTable


class User(BaseModel):
    '''Модель пользователя'''
    username: str
    email: str
    password: str

class Post(BaseModel):
    '''Модель постов'''
    title: str
    content: str
    user_id: int


class UserRepository:
    '''Методы для работы с бд пользователей'''
    @classmethod
    async def add_one(cls, data: User) -> int:
        '''Добавляет пользователя'''
        async with new_session() as session:

            user = UserTable(
                username=data.username,
                email=data.email,
                password=data.password
            )

            session.add(user)
            await session.flush()
            await session.commit()
            return user.id

    @classmethod
    async def get_all(cls):
        '''Возвращает данные обо всех пользователях'''
        async with new_session() as session:
            query = select(UserTable)
            result = await session.execute(query)
            user_models = result.scalars().all()
            return user_models

    @classmethod
    async def update_email(cls, user_id: int, new_email: str):
        '''Обновляет email пользователя'''
        async with new_session() as session:
            query = update(UserTable).where(UserTable.id == user_id).values(email=new_email)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, user_id: int):
        '''Удаляет пользователя и все его посты'''
        async with new_session() as session:
            query = (
                select(UserTable)
                .where(UserTable.id == user_id)
                .options(joinedload(UserTable.posts)))
            user = await session.scalar(query)
            await session.delete(user)
            await session.commit()


class PostRepository:
    '''Методы для работы с бд постов'''
    @classmethod
    async def add_one(cls, data: Post) -> int:
        '''Добавляет пост'''
        async with new_session() as session:

            post = PostTable(
                title=data.title,
                content=data.content,
                user_id=data.user_id
            )

            session.add(post)
            await session.flush()
            await session.commit()
            return post.id

    @classmethod
    async def get_all(cls):
        '''Возвращает данные обо всех постах вместе с их пользователями'''
        async with new_session() as session:
            query = select(PostTable).options(joinedload(PostTable.user))
            result = await session.execute(query)
            post_models = result.scalars().all()
            return post_models

    @classmethod
    async def get_posts(cls, user_id: int):
        '''Возвращает все посты конкретного пользователя'''
        async with new_session() as session:
            query = select(PostTable).where(PostTable.user_id == user_id)
            result = await session.execute(query)
            post_models = result.scalars().all()
            return post_models

    @classmethod
    async def update_content(cls, post_id: int, new_content: str):
        '''Обновляет content пользователя'''
        async with new_session() as session:
            query = update(PostTable).where(PostTable.id == post_id).values(content=new_content)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, post_id: int):
        '''Удаляет пост'''
        async with new_session() as session:
            query = delete(PostTable).where(PostTable.id == post_id)
            await session.execute(query)
            await session.commit()
