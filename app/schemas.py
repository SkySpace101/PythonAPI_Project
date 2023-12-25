from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title:str
    content:str
    published:bool = False

class PostCreate(PostBase):
    pass

# we are gonna create a class for our reponse
# this configuration class will make the orm model response to pydantic model response.

class Post(PostBase):
    pass
    # id: int
    # created_at: datetime

    class Config:
        orm_mode = True
