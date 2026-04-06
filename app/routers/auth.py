from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserLogin, UserResponse
from app.services.user_service import UserService
from app.middleware.auth_middleware import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=dict)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login endpoint - returns user info and user ID for subsequent requests
    
    In a production system, this would return a JWT token.
    For this demo, clients should use the returned user_id in X-User-Id header.
    """
    user = UserService.authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    return {
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username,
        "role": user.role.value,
        "instruction": "Use the user_id in X-User-Id header for subsequent requests"
    }


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """
    Logout endpoint
    
    In a production system with JWT, this would invalidate the token.
    For this demo, client should simply stop sending X-User-Id header.
    """
    return {
        "message": "Logout successful"
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information
    """
    return current_user
