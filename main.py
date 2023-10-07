from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


# Validation for the Post Requests (Creating a Schema using Pydantic)
class Post(BaseModel):
    title:str
    content:str
    published:bool = False
    rating: Optional[int] = None


app = FastAPI()

my_posts = [{"title":"This is post-1","content":"content of post-1", "id":1}, \
             {"title":"This is post-2","content":"content of post-2", "id":2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts")
async def post_created(new_post: Post):
    new_post = new_post.model_dump()
    new_post['id'] = randrange(0,1000000)
    my_posts.append(new_post)
    return {"data": new_post}

@app.get("/posts/{id}")
async def get_post(id:int):
    post = find_post(id)
    # return {"data": f"The post you requested {id}"}
    return {"data": post}

