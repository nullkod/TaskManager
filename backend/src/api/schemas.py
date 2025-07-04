from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# --- User ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

    model_config = ConfigDict(extra='forbid')

class UserRead(UserBase):
    id: int


# --- Task ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None

class TaskRead(TaskBase):
    id: int
    status: bool
    created_at: datetime
    owner_id: int