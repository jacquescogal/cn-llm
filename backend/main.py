from fastapi import FastAPI
from src.routers import *
app = FastAPI()

app.include_router(word_router)
app.include_router(card_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}