from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random
import string


# Validation for the Post Requests (Creating a Schema using Pydantic)
class Post(BaseModel):
    title:str
    content:str
    published:bool = False
    rating: Optional[int] = None

with open("book.txt",encoding="UTF-8") as f:
    word_bag = f.read().split(" ")
    random.shuffle(word_bag)

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/posts")
async def randomMsg():
    return {"post": "".join([random.choice(string.ascii_letters) for i in range(50)])}

@app.get("/passage")
async def cryptic_msg ():
    return {"msg": " ".join([random.choice(word_bag) for i in range(200)])}

@app.post("/create")
async def post_created(payload: Post):
    print(payload)
    # return {"data": "This is the data"}
    return {"title":payload.title, "Content": payload.content}
