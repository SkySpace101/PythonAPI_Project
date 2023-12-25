from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
import time
import models
from database import engine, get_db
from sqlalchemy.orm import Session
import schemas

# Adding the ORM to our main app file
models.Base.metadata.create_all(bind=engine)

# creating a fastapi app.
app = FastAPI()

# Routes

@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def post_created(post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.model_dump())

    # need to add the data to out database
    db.add(new_post)

    # commit all the changes to the database
    db.commit()

    # getting returned post
    db.refresh(new_post)

    return new_post

@app.get("/posts/latest", response_model=schemas.Post)
async def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return post


@app.get("/posts/{id}", response_model=schemas.Post)
async def get_post(id:int, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
        if (post == None):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} was not found.")
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} was not found.")
    
    return post

# Deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db) ):
    post = db.query(models.Post).filter(models.Post.id == id) 
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"The post with id: {id} was not found.")
    
    post.delete(synchronize_session=False)
    db.commit()

# Updating the Post
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
async def update_post(id: int, update_post: schemas.PostBase, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"The post with id: {id} was not found.")
    
    # post.update({"title": "this is the new title", "content": "this is the new content"}, synchronize_session=False)
    post.update(update_post.model_dump(), synchronize_session=False)

    # commit all the changes
    db.commit()

    # return {"message": "updated post Successfully"}
    return post.first()




