from fastapi import FastAPI
from .database import Base, engine
from .routers.auth import router as auth_router
from .routers.pdf import router as pdf_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(pdf_router)

@app.get("/")
def home():
    return {"message": "Hello world"}
