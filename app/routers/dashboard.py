from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.database import get_db
from app.services.dashboard_service import DashboardService
from app.middleware.auth_middleware import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=Dict[str, Any])
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get overall financial summary (All roles)
    
    Returns:
    - Total income
    - Total expenses
    - Net balance
    - Record counts
    """
    return DashboardService.get_overall_summary(db)


@router.get("/by-category", response_model=Dict[str, Any])
def get_category_breakdown(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get category-wise financial breakdown (All roles)
    
    Returns income and expenses grouped by category
    """
    return DashboardService.get_category_summary(db)


@router.get("/recent", response_model=Dict[str, Any])
def get_recent_activity(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get recent financial activity (All roles)
    
    Returns the most recent financial records
    """
    return {
        "recent_records": DashboardService.get_recent_activity(db, limit)
    }


@router.get("/trends", response_model=Dict[str, Any])
def get_trends(
    months: int = Query(6, ge=1, le=24),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get monthly financial trends (All roles)
    
    Returns income, expenses, and net balance trends over specified months
    """
    return DashboardService.get_monthly_trends(db, months)


@router.get("/weekly", response_model=Dict[str, Any])
def get_weekly_summary(
    weeks: int = Query(4, ge=1, le=52),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get weekly financial summary (All roles)
    
    Returns aggregated data for the specified number of weeks
    """
    return DashboardService.get_weekly_summary(db, weeks)
