from fastapi import APIRouter, status, Depends, HTTPException
import database
import schemas, models
from sqlalchemy.orm import Session
import utils


router = APIRouter(tags=["Authentication"])

@router.post("/login")
async def login(user_credentials : schemas.UserLogin, db: Session = Depends(database.get_db) ):

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details = "Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details = "Invalid Credentials")
    
    # create token
    # return token
    return {"token": "example token"}

    
