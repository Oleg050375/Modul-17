from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///taskmanager.db')  # создание движка

SessionLocal = sessionmaker(bind=engine)  # создание сессии связи с БД

class Base(DeclarativeBase):  # создание базового класса
    pass

