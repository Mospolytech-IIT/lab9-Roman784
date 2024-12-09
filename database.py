'''database.py'''


from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column


class BaseTable(DeclarativeBase):
    '''База для всех таблиц'''
    pass

class UserTable(BaseTable):
    '''Таблица пользователя'''
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    posts: Mapped[list['PostTable']] = relationship('PostTable', back_populates='user', cascade="all, delete-orphan")

class PostTable(BaseTable):
    '''Таблица постов'''
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['UserTable'] = relationship('UserTable', back_populates='posts')


engine = create_async_engine('sqlite+aiosqlite:///database.db')
new_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_tables():
    '''Создаёт таблицы'''
    async with engine.begin() as conn:
        await conn.run_sync(BaseTable.metadata.create_all)
        print("create")

async def delete_tables():
    '''Удаляет таблицы'''
    async with engine.begin() as conn:
        await conn.run_sync(BaseTable.metadata.drop_all)
        print("delete")
