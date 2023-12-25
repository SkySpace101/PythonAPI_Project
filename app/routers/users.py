from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import models, schemas, utils
from sqlalchemy.orm import Session
from database import get_db

# Creating a router object
router = APIRouter()

# All user related routes

# creating the user 
@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # creating the hash of the password using the password context object we created previously.
    hashed_password = utils.hash(user.password)

    # then we are storing this hashed password to user.password
    user.password = hashed_password

    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/users/{id}" , response_model=schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, \
                            detail={f"The user with id {id} does not exit"})
    
    return user