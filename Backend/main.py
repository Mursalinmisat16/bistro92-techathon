from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel


from database import engine
from routers import order


app = FastAPI(titile = 'BESTRO 92 Backend')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    
    
app.include_router(order.router)

@app.get("/")
def test():
    return "working"