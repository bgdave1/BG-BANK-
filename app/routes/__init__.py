from fastapi import APIRouter
from app.routes import auth, bank

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(bank.router, prefix="/bank", tags=["Bank"])
