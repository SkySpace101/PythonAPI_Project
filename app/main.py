from fastapi import FastAPI, Response, status, HTTPException
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
    id: int 

# To be safe from client side intrusion and attacks it's better to have a
#  data validation in place when asking the client for data.

app = FastAPI()

my_posts = [{"title":"This is post-1","content":"content of post-1", "id":1}, \
             {"title":"This is post-2","content":"content of post-2", "id":2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_post_index(id):
     for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def post_created(new_post: Post):
    new_post = new_post.model_dump()
    new_post['id'] = randrange(0,1000000)
    my_posts.append(new_post)
    return {"data": new_post}

@app.get("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"data": post}


@app.get("/posts/{id}")
# async def get_post(id:int, response: Response):
async def get_post(id:int):
    post = find_post(id)
    # return {"data": f"The post you requested {id}"}
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"The post with id {id} was not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} was not found.")

    return {"data": post}

# Deleting a post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_post_index(id)
    if(index == None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"The post with id: {id} was not found.")
    my_posts.pop(index)
    Response(status_code=status.HTTP_204_NO_CONTENT)

# Updating the Post

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(id: int, post: Post):
    # print(post)
    index = find_post_index(id)
    if(index == None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"The post with id: {id} was not found.")

    post_dict = post.model_dump()
    my_posts[index] = post_dict

    return {"message": "updated post Successfully"}



