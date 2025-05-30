from fastapi import APIRouter
from app.api.v1.endpoints import assets_router, auth_router, users_router

api_router = APIRouter()

api_router.include_router(assets_router, prefix="/assets", tags=["assets"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"]) 