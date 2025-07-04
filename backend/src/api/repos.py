from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from api.models import User, Task
from api.schemas import UserCreate
from sqlalchemy import select

from api.auth import oauth2_scheme, SECRET_KEY, ALGORITHM

class BaseRepository(ABC):
    """Интерфейс для репозиториев"""

    def __init__(self, session: AsyncSession | Session):
        self.session = session

    @abstractmethod
    def get_by_id(self, id: int):
        pass

    @abstractmethod
    def get_all(self, user_id: int, offset: int, limit: int):
        pass

    @abstractmethod
    def create(self, data: dict):
        pass

    @abstractmethod
    def update(self, id: int, data: dict):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass

class TaskRepo(BaseRepository):
    """Репозиторий для работы с задачами"""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, user_id: int, offset: int, limit: int):
        stmt = select(Task).filter(Task.owner_id == user_id).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, task_id: int):
        stmt = select(Task).filter(Task.id == task_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, data: dict):
        db_task = Task(**data)
        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)
        return db_task
    
    async def update(self, task_id: int, data: dict):
        db_task = await self.get_by_id(task_id)
        for field, value in data.items():
            setattr(db_task, field, value)
        
        await self.session.commit()
        await self.session.refresh(db_task)
        return db_task
    
    async def delete(self, task_id: int):
        db_task = await self.get_by_id(task_id)
        await self.session.delete(db_task)
        await self.session.commit()
        return db_task

class UserRepo(BaseRepository):
    """Репозиторий для работы с пользователями"""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int):
        stmt = select(User).filter(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(self):
        stmt = select(User)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def create(self, data: dict):
        db_user = User(**data)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user
    
    async def update(self, user_id: int, data: dict):
        pass
    
    async def delete(self, user_id: int):
        db_user = await self.get_by_id(user_id)
        await self.session.delete(db_user)
        await self.session.commit()
        return db_user
        
    async def get_user_by_username(self, username: str):
        """Получение пользователя по username"""
        stmt = select(User).filter(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
