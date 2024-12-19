from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])

DbSession = Annotated[Session, Depends(get_db)]


@router.get('/', response_model=list[User])
async def get_all_users(db: DbSession):
    query = text('SELECT * FROM users')
    result = db.execute(query).fetchall()
    return [User(id=row.id, name=row.username, slug=row.slug) for row in result]


@router.get('/user_id', response_model=list[User])
async def user_by_id(user_id: int, db: DbSession):
    query = text('SELECT * FROM users WHERE id = :id')
    result = db.execute(query, {'id': user_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail='User not found')
    return User(id=result.id, name=result.username, slug=result.slug)


@router.post('/create', response_model=User)
async def create_user(user: CreateUser, db: DbSession):
    query = text('INSERT INTO users(username, slug) VALUES (:username, :slug)')
    db.execute(query, {'username': user.username, 'slug': user.slug})
    db.commit()
    select_query = text('SELECT * FROM users WHERE username = :username')
    result = db.execute(select_query, {'username': user.username}).fetchone()
    return User(id=result.id, username=result.username, slug=result.slug)


@router.put('/update', response_model=User)
async def update_user(user_id: int, user: UpdateUser, db: DbSession):
    select_query = text('SELECT * FROM users WHERE id = :id')
    result = db.execute(select_query, {'id': user_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail='User not found')
    update_query = text('UPDATE users SET username = :username, slug = :slug WHERE id = :id')
    db.execute(update_query, {'id': user.id, 'username': user.username, 'slug': user.slug}, )
    db.commit()
    updated_result = db.execute(select_query, {'id': user_id}).fetchone()
    return User(id=updated_result.id, username=updated_result.username, slug=updated_result.slug)


@router.delete('/delete', response_model=User)
async def delete_user(user_id: int, db: DbSession):
    select_query = text('SELECT * FROM users WHERE id = :id')
    result = db.execute(select_query, {'id': user_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail='User not found')
    delete_query = text('DELETE FROM users WHERE id = :id')
    db.execute(delete_query, {'id': user_id})
    db.commit()
    return {'message': 'User deleted'}
