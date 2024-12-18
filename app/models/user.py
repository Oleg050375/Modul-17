from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db import Base
from app.models.task import Task


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer, default=0)
    slug = Column(String, unique=True, index=True)


tasks = relationship('Task', back_populates='users')  # связь с таблицей Task
