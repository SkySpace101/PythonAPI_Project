# Every python model represents a table in the database.
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, TIMESTAMP, text

class Post(Base):
    # Naming the table
    __tablename__ = "pst"

    id = Column(Integer, primary_key= True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = 'True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text('now()'))



#Random Table for fun
# class Toast(Base):

#     #naming the model
#     __tablename__ = "toast"

#     SerialNo = Column(Integer, primary_key=True, nullable=False)
#     Name = Column(String, nullable = False)
#     Marks1 = Column(Float, nullable=False)
#     Marks2 = Column(Float, nullable=False)
#     Pass = Column(Boolean, nullable=False, default=True)

    