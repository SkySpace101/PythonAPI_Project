from fastapi import FastAPI
import random
import string

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/posts")
async def randomMsg():
    return {"post": "".join([random.choice(string.ascii_letters) for i in range(50)])}