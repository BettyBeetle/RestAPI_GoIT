from fastapi import FastAPI
from fastapi.routing import APIRouter

from m11.routes import contacts

app = FastAPI()

docs_router = APIRouter()

app.include_router(docs_router)
app.include_router(contacts.router, prefix='/api', tags=["contacts"])