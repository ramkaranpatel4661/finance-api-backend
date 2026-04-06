from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Service class for user management operations"""

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        try:
            user = User(
                username=user_data.username,
                email=user_data.email,
                role=user_data.role,
                is_active=user_data.is_active
            )
            user.set_password(user_data.password)
            
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError as e:
            db.rollback()
            if "username" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
            elif "email" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not create user"
            )

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
        """Update user information"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        update_data = user_data.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            user.set_password(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(user, field, value)

        try:
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError as e:
            db.rollback()
            if "email" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not update user"
            )

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete (deactivate) a user"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.is_active = False
        db.commit()
        return True

    @staticmethod
    def update_user_role(db: Session, user_id: int, new_role: UserRole) -> User:
        """Update user role"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.role = new_role
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        user = UserService.get_user_by_username(db, username)
        if not user or not user.is_active:
            return None
        if not user.verify_password(password):
            return None
        return user
