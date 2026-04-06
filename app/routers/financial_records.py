from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.financial_record import (
    FinancialRecordCreate,
    FinancialRecordUpdate,
    FinancialRecordResponse,
    FinancialRecordFilter
)
from app.services.financial_service import FinancialRecordService
from app.middleware.auth_middleware import get_current_user, require_admin
from app.models.user import User, UserRole

router = APIRouter(prefix="/api/records", tags=["Financial Records"])


@router.post("/", response_model=FinancialRecordResponse, status_code=status.HTTP_201_CREATED)
def create_record(
    record_data: FinancialRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new financial record (Analyst and Admin only)
    """
    if current_user.role == UserRole.VIEWER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Viewers cannot create records"
        )
    
    return FinancialRecordService.create_record(db, record_data, current_user.id)


@router.get("/", response_model=List[FinancialRecordResponse])
def list_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    type: Optional[str] = None,
    category: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all financial records with optional filters (All roles)
    """
    # Build filter object
    filters = FinancialRecordFilter(
        type=type,
        category=category,
        date_from=date_from,
        date_to=date_to,
        min_amount=min_amount,
        max_amount=max_amount
    )
    
    return FinancialRecordService.get_all_records(db, filters, skip, limit)


@router.get("/{record_id}", response_model=FinancialRecordResponse)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get financial record by ID (All roles)
    """
    record = FinancialRecordService.get_record_by_id(db, record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial record not found"
        )
    return record


@router.put("/{record_id}", response_model=FinancialRecordResponse)
def update_record(
    record_id: int,
    record_data: FinancialRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Update financial record (Admin only)
    """
    return FinancialRecordService.update_record(db, record_id, record_data)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete financial record (Admin only)
    """
    FinancialRecordService.delete_record(db, record_id)
    return None
