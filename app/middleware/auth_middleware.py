from fastapi import HTTPException, status, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.models.user import User, UserRole


def get_current_user(
    x_user_id: Optional[int] = Header(None, description="User ID for authentication"),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from header
    For demo purposes, we use X-User-Id header
    In production, this would validate JWT tokens
    """
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide X-User-Id header."
        )
    
    user = db.query(User).filter(User.id == x_user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


def require_role(allowed_roles: List[UserRole]):
    """
    Dependency to check if current user has required role
    Usage: require_role([UserRole.ADMIN, UserRole.ANALYST])
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {', '.join([r.value for r in allowed_roles])}"
            )
        return current_user
    
    return role_checker


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Shortcut dependency for admin-only routes"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def require_analyst_or_admin(current_user: User = Depends(get_current_user)) -> User:
    """Shortcut dependency for analyst or admin routes"""
    if current_user.role not in [UserRole.ANALYST, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analyst or Admin access required"
        )
    return current_user
