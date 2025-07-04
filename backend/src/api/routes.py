from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import List
from api.services import TaskService, UserService, get_task_service, get_user_service
from core.database import get_async_session
from api.models import User, Task
from api.schemas import UserCreate, UserRead, TaskCreate, TaskUpdate, TaskRead
from fastapi.security import OAuth2PasswordRequestForm
from api import auth

router = APIRouter()


# --- Работа с пользователями ---
@router.post("/register", response_model=UserRead)
async def new_register(user: UserCreate, service: UserService = Depends(get_user_service), 
    user_service: UserService = Depends(get_user_service)):

    """
    Регистрация пользователя
    """

    db_user = await user_service.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username уже занят")

    hashed_password = auth.password_hash(user.password)
    user_data = {'username': user.username, 'hashed_password': hashed_password}
    new_user = await service.create(user_data)
    return new_user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), 
    user_service: UserService = Depends(get_user_service)):
    """
    Логин пользователя
    """
    user = await user_service.get_user_by_username(form_data.username)
    user = auth.authenticate_user(form_data.username, form_data.password, user)
    if not user:
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}



# ----- Задачи -----
@router.get("/tasks", response_model=List[TaskRead])
async def read_tasks(offset: int = 0, limit: int = 100, service: TaskService = Depends(get_task_service), current_user: User = Depends(auth.get_current_user)):
    """
    Получение всех задач
    """
    print(current_user.id)
    return await service.get_all(user_id=current_user.id, offset=offset, limit=limit)

@router.post("/tasks", response_model=TaskRead)
async def create_task(task: TaskCreate, service: TaskService = Depends(get_task_service), current_user: User = Depends(auth.get_current_user)):
    """
    Создание задачи
    """
    task_data = task.model_dump()
    task_data['owner_id'] = current_user.id
    print(task_data)
    return await service.create(task_data)


@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, updates: TaskUpdate, service: TaskService = Depends(get_task_service), current_user: User = Depends(auth.get_current_user)):
    """
    Обновление задачи
    """
    db_task = await service.get_by_id(task_id)
    print('----------------Update task----------------', updates.title, updates.description, updates.status)
    if not db_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return await service.update(db_task.id, updates.model_dump())

@router.delete("/tasks/{task_id}", response_model=TaskRead)
async def delete_task(task_id: int, service: TaskService = Depends(get_task_service), current_user: User = Depends(auth.get_current_user)):
    """
    Удаление задачи
    """
    return await service.delete(task_id)