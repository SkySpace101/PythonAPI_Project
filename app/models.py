# ORM Models
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, TIMESTAMP, text

class Post(Base):
    __tablename__ = "pst"

    id = Column(Integer, primary_key= True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = 'True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('now()'))


# Creating a user table model for user registration
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, nullable = False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('now()'))
    