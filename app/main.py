from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
import time
import models
from database import engine, get_db
from sqlalchemy.orm import Session

# Adding the ORM to our main app file
models.Base.metadata.create_all(bind=engine)


# Validation for the Post Requests (Creating a Schema using Pydantic)
class Post(BaseModel):
    # id: int 
    title:str
    content:str
    published:bool = False
    # rating: Optional[int] = None
    

# To be safe from client side intrusion and attacks it's better to have a
#  data validation in place when asking the client for data.

app = FastAPI()

my_posts = [{"title":"This is post-1","content":"content of post-1", "id":1}, \
             {"title":"This is post-2","content":"content of post-2", "id":2}]


# database connection and Stuff

while True:
    try:
        conn = psycopg2.connect(host="localhost",database='fastapi',user='postgres', password='admin')
        cursor = conn.cursor()
        print("database connection established")
        break;
    except Exception as Error:
        print("The connection to database not established")
        time.sleep(2)


# cursor.execute("SELECT * FROM posts")
# cursor.execute("INSERT INTO posts(title,content) VALUES ('this is post-4','This is content of fourth post') RETURNING *;")
# # cursor.fetchall();
# conn.commit()
# cursor.close()
# conn.close()
# print("The database connection is closed")


# Utility functions

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
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()

    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def post_created(post: Post, db: Session = Depends(get_db)):
    # new_post = new_post.model_dump()
    # new_post['id'] = randrange(0,1000000)
    # my_posts.append(new_post)
    # cursor.execute("INSERT INTO posts(title,content) VALUES (%s,%s)",vars=(new_post.title,new_post.content))
    # conn.commit()

    # We are creating the new post from the payload from the endpoint
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    # there's an issue with previous line as if we have hundreds of filed it will become very combursome to write all this stuff so what follows will be done.
    # print(**post.model_dump()) <-- we unpack the post dictionary using '**' operator

    new_post = models.Post(**post.model_dump())

    # need to add the data to out database
    db.add(new_post)

    # commit all the changes to the database
    db.commit()

    # getting returned post
    db.refresh(new_post)

    return {"data": new_post}

@app.get("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"data": post}


@app.get("/posts/{id}")
# async def get_post(id:int, response: Response):
async def get_post(id:int):
    # post = find_post(id)
    # return {"data": f"The post you requested {id}"}
    print(id)
    try:
        cursor.execute("SELECT * FROM posts WHERE id = %s", str(id))
        post = cursor.fetchone()
        # if (post == None):
            # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} was not found.")
        # print(post)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} was not found.")
    

    # if not post:
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"message":f"The post with id {id} was not found."}
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} was not found.")

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

# defining a get route to test the db ORM.
@app.get("/sqlalchemy")
async def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data": posts}

    # the below code simply return raw SQL Code that was abstracted via ORM
    # posts = db.query(models.Post)
    # print(posts)
    # return {"status": "success"}




