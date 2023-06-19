from fastapi import FastAPI
from config.database import Base
from config.database import engine
from routers import document_router, user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.include_router(document_router.router)
# app.include_router(user_router.router)

