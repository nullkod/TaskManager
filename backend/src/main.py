from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os

from core.config import settings
from core.base_model import Base
from core.database import engine
from api.routes import router as task_router


def create_tables():
    Base.metadata.create_all(bind=engine)

def clean_database():
    try:
        if os.path.exists("test.db"):
            os.remove("test.db")
            print("База данных очищена")
    except Exception as e:
        print(f"Ошибка при очистке базы данных: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # создание таблиц при запуске приложения
    create_tables()
    yield
    # удаляем бд при завершении приложения
    # clean_database()




app = FastAPI(lifespan=lifespan)

# Подключаем роуты
app.include_router(task_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
