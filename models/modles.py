from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    username = Column(String)
    telegramid = Column(BigInteger, primary_key=True)

    tasks = relationship("Task", back_populates="user")


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    user_telegramid = Column(BigInteger, ForeignKey('users.telegramid'))
    status = Column(Boolean,default=False  )

    user = relationship("User", back_populates="tasks")
