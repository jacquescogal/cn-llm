from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controllers import *
app = FastAPI()

app.include_router(word_controller)
app.include_router(card_controller)
app.include_router(review_controller)

# add cors  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}