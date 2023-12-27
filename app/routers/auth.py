from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm # using this utility provided by fastapi to get user credentials (username and password) here username and password can be any field. 
import database
import schemas, models
from sqlalchemy.orm import Session
import utils, oauth2


router = APIRouter(tags=["Authentication"])

@router.post("/login")
async def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db) ):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details = "Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details = "Invalid Credentials")
    
    # create token
    # creating a token using the oauth with the data that we decide - in this case a user id.
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # return token
    return {"access_token" : access_token, "token_type": "bearer"}

    
