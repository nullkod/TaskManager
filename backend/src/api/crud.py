from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.models import Task
from api.schemas import TaskCreate, TaskUpdate


async def get_tasks(session: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    stmt = select(Task).filter(Task.owner_id == user_id).offset(skip).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_task(session: AsyncSession, task_id: int, user_id: int):
    stmt = select(Task).filter(Task.id == task_id, Task.owner_id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def create_task(session: AsyncSession, task: TaskCreate, user_id: int):
    db_task = Task(**task.model_dump(), owner_id=user_id)
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task

async def update_task(session: AsyncSession, db_task: Task, updates: TaskUpdate):
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)
    await session.commit()
    await session.refresh(db_task)
    return db_task

async def delete_task(session: AsyncSession, db_task: Task):
    await session.delete(db_task)
    await session.commit()
