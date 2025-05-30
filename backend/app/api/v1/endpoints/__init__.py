"""
API endpoints package
"""

from .assets import router as assets_router
from .auth import router as auth_router
from .users import router as users_router

__all__ = ["assets_router", "auth_router", "users_router"] 