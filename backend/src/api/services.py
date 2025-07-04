import select
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from api.repos import BaseRepository, TaskRepo, UserRepo
from api.schemas import TaskCreate
from api.auth import get_username, oauth2_scheme
from api.models import User
from core.database import get_async_session, get_session
from abc import ABC, abstractmethod

class BaseService(ABC):
    """Интерфейс для сервисов"""

    def __init__(self, repo: BaseRepository):
        self.repo = repo

    @abstractmethod
    def get_by_id(self, id: int):
        pass

    @abstractmethod
    def get_all(self):
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


class TaskService(BaseService):
    """Сервис для работы с задачами"""

    def __init__(self, repo: TaskRepo):
        self.repo = repo

    async def get_by_id(self, task_id: int):
        return await self.repo.get_by_id(task_id)
    
    async def get_all(self, user_id: int, offset: int, limit: int):
        return await self.repo.get_all(user_id, offset, limit)
    
    async def create(self, data: dict):
        return await self.repo.create(data)
    
    async def update(self, task_id: int, data: dict):
        return await self.repo.update(task_id, data)
    
    async def delete(self, task_id: int):
        return await self.repo.delete(task_id) 


class UserService(BaseService):
    """Сервис для работы с пользователями"""

    def __init__(self, repo: UserRepo):
        self.repo = repo

    async def get_by_id(self, user_id: int):
        return await self.repo.get_by_id(user_id)
    
    async def get_all(self):
        return self.repo.get_all()
    
    async def create(self, data: dict):
        return await self.repo.create(data)
    
    async def update(self, user_id: int, data: dict):
        return await self.repo.update(user_id, data)
    
    async def delete(self, user_id: int):
        return await self.repo.delete(user_id)
    
    async def get_user_by_username(self, username: str) -> User | None:
        return await self.repo.get_user_by_username(username)
    
        
def get_task_service(session: AsyncSession = Depends(get_async_session)):
    return TaskService(TaskRepo(session))

def get_user_service(session: AsyncSession = Depends(get_async_session)):
    return UserService(UserRepo(session))