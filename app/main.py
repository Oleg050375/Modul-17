from fastapi import FastAPI
from routers import task, user  # импорт объектов роутеров

app = FastAPI()

@app.get('/')
async def welcome():
    return {'message':'Welcome to Taskmanager'}

app.include_router(task.router)  # подключение роутера задач
app.include_router(user.router)  # подключение роутера пользователей
