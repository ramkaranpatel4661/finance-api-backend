from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService
from app.middleware.auth_middleware import require_admin, get_current_user
from app.models.user import User, UserRole

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create a new user (Admin only)
    """
    return UserService.create_user(db, user_data)


@router.get("/", response_model=List[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    List all users (Admin only)
    """
    return UserService.get_all_users(db, skip, limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Get user by ID (Admin only)
    """
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Update user information (Admin only)
    """
    return UserService.update_user(db, user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Deactivate user (Admin only)
    """
    UserService.delete_user(db, user_id)
    return None


@router.put("/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    new_role: UserRole,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Update user role (Admin only)
    """
    return UserService.update_user_role(db, user_id, new_role)
