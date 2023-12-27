from jose import JWTError, jwt
from datetime import datetime, timedelta

 
# SECRET_KEY to be used to create the token
# ALOGIRITHM to create token
# Expiration Date of Token

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# function to create access token
def create_access_token(data: dict):
    
    # create a copy of the data that we get since we need to manipulate it.
    to_encode = data.copy()

    # setting the expiration time
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Adding the expire time to the to_encode dictionary.
    to_encode.update({"exp": expire})

    # creating the jwt encoded token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

