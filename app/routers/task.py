from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import Task
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])

DbSession = Annotated[Session, Depends(get_db)]

@router.get('/', response_model=list[Task])
async def get_all_tasks(db: DbSession):
    query = text('SELECT * FROM tasks')
    result = db.execute(query).fetchall()
    return [Task(id=row.id, name=row.username, slug=row.slug) for row in result]

@router.get('/task_id', response_model=list[Task])
async def task_by_id(task_id: int, db: DbSession):
    query = text('SELECT * FROM tasks WHERE id = :id')
    result = db.execute(query, {'id': task_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail='Task not found')
    return Task(id=result.id, name=result.username, slug=result.slug)

@router.post('/create', response_model=Task)
async def create_task(task: CreateTask, db: DbSession):
    query = text('INSERT INTO tasks(taskname, slug, user_id) VALUES (:taskname, :slug, :user_id')
    db.execute(query, {'taskname': task.username, 'slug': task.slu, 'user_id': task.user_id})
    db.commit()
    select_query = text('SELECT * FROM tasks WHERE taskname = :taskname AND slug = :slug')
    result = db.execute(select_query, {'taskname': task.taskname, 'slug': task.slug}).fetchone()
    return Task(id=result.id, taskname=result.taskname, slug=result.slug, user_id=result.user_id)

@router.put('/update', response_model=Task)
async def update_task(task_id: int, task: UpdateTask, db: DbSession):
    select_query = text('SELECT * FROM tasks WHERE id = :id')
    result = db.execute(select_query, {'id': task_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail='User not found')
    update_query = text('UPDATE tasks SET taskname = :taskname, slug = :slug WHERE id = :id')
    db.execute(update_query, {'id': task.id, 'username': task.username, 'slug': task.slug}, )
    db.commit()
    updated_result = db.execute(select_query, {'id': task_id}).fetchone()
    return Task(id=updated_result.id, username=updated_result.username, slug=updated_result.slug)

@router.delete('/delete', response_model=Task)
async def delete_task(task_id: int, db: DbSession):
    select_query = text('SELECT * FROM tasks WHERE id = :id')
    result = db.execute(select_query, {'id': task_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail='Task not found')
    delete_query = text('DELETE FROM tasks WHERE id = :id')
    db.execute(delete_query, {'id': task_id})
    db.commit()
    return {'message': 'Task deleted'}
