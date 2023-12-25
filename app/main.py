from fastapi import FastAPI
from typing import  List
import models
from database import engine
from routers import post, users

models.Base.metadata.create_all(bind=engine)

# creating a fastapi app.
app = FastAPI()

# Routes

# using router object from the routers folder to get the specific route
app.include_router(post.router)
app.include_router(users.router)


# simple route
@app.get("/")
async def root():

    return {"message":"Hello World"}





