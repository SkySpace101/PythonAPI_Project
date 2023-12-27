from fastapi import status, HTTPException, Depends, APIRouter
import models, schemas
from database import get_db
from typing import  List
from sqlalchemy.orm import Session


# Creating a router object
router = APIRouter(prefix="/posts", 
                   tags = ['Posts'])


# all post related routes

# Getting all posts
@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return posts


# Creating a Post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def post_created(post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.model_dump())

    # need to add the data to out database
    db.add(new_post)

    # commit all the changes to the database
    db.commit()

    # getting returned post
    db.refresh(new_post)

    return new_post

# Getting a post
@router.get("/{id}", response_model=schemas.Post)
async def get_post(id:int, db: Session = Depends(get_db)):

    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()

        if (post == None):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  \
                                detail=f"The post with id {id} was not found.")
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, \
                             detail=f"The post with id {id} was not found.")
    
    return post


# Deleting a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db) ):

    post = db.query(models.Post).filter(models.Post.id == id) 

    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"The post with id: {id} was not found.")
    
    post.delete(synchronize_session=False)

    db.commit()


# Updating the Post
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
async def update_post(id: int, update_post: schemas.PostBase, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"The post with id: {id} was not found.")
    
    # running update post query
    post.update(update_post.model_dump(), synchronize_session=False)

    # commit all the changes
    db.commit()

    # return {"message": "updated post Successfully"}
    return post.first()
