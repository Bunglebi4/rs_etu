from database import Base, engine
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    session_token = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)