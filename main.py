from fastapi import FastAPI
import random
import string

with open("book.txt",encoding="UTF-8") as f:
    word_bag = f.read().split(" ")
    random.shuffle(word_bag)

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/posts")
async def randomMsg():
    return {"post": "".join([random.choice(string.ascii_letters) for i in range(50)])}

@app.get("/passage")
async def cryptic_msg ():
    return {"msg": " ".join([random.choice(word_bag) for i in range(200)])}
