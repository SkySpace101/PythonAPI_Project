from pydantic import BaseModel

# To be safe from client side intrusion and attacks it's better to have a
#  data validation in place when asking the client for data.

# Validation for the Post Requests (Creating a Schema using Pydantic)
class PostBase(BaseModel):
    # id: int 
    title:str
    content:str
    published:bool = False
    # rating: Optional[int] = None

# inheriting from a pydantic class model 
class PostCreate(PostBase):
    pass

# it is better to seprate the class/model schemas for different routes or functions.