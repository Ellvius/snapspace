from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import environment

app = FastAPI(title="SnapSpace")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(environment.router)

@app.get('/')
def read_root():
    return { "message" : "Dev Environment platform API"}