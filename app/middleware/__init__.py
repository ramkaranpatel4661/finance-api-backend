"""
Middleware initialization
"""
from app.middleware.auth_middleware import get_current_user, require_role

__all__ = ["get_current_user", "require_role"]
