from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Dict, List, Any
from datetime import date, datetime, timedelta
from decimal import Decimal
from app.models.financial_record import FinancialRecord, RecordType


class DashboardService:
    """Service class for dashboard analytics and summaries"""

    @staticmethod
    def get_overall_summary(db: Session) -> Dict[str, Any]:
        """Get overall financial summary"""
        # Calculate total income
        total_income = db.query(func.sum(FinancialRecord.amount)).filter(
            FinancialRecord.type == RecordType.INCOME
        ).scalar() or Decimal('0')

        # Calculate total expenses
        total_expenses = db.query(func.sum(FinancialRecord.amount)).filter(
            FinancialRecord.type == RecordType.EXPENSE
        ).scalar() or Decimal('0')

        # Calculate net balance
        net_balance = total_income - total_expenses

        # Count records
        total_records = db.query(func.count(FinancialRecord.id)).scalar() or 0
        income_count = db.query(func.count(FinancialRecord.id)).filter(
            FinancialRecord.type == RecordType.INCOME
        ).scalar() or 0
        expense_count = db.query(func.count(FinancialRecord.id)).filter(
            FinancialRecord.type == RecordType.EXPENSE
        ).scalar() or 0

        return {
            "total_income": float(total_income),
            "total_expenses": float(total_expenses),
            "net_balance": float(net_balance),
            "total_records": total_records,
            "income_count": income_count,
            "expense_count": expense_count
        }

    @staticmethod
    def get_category_summary(db: Session) -> Dict[str, Any]:
        """Get category-wise financial summary"""
        # Income by category
        income_by_category = db.query(
            FinancialRecord.category,
            func.sum(FinancialRecord.amount).label('total'),
            func.count(FinancialRecord.id).label('count')
        ).filter(
            FinancialRecord.type == RecordType.INCOME
        ).group_by(FinancialRecord.category).all()

        # Expenses by category
        expenses_by_category = db.query(
            FinancialRecord.category,
            func.sum(FinancialRecord.amount).label('total'),
            func.count(FinancialRecord.id).label('count')
        ).filter(
            FinancialRecord.type == RecordType.EXPENSE
        ).group_by(FinancialRecord.category).all()

        return {
            "income_by_category": [
                {
                    "category": cat,
                    "total": float(total),
                    "count": count
                }
                for cat, total, count in income_by_category
            ],
            "expenses_by_category": [
                {
                    "category": cat,
                    "total": float(total),
                    "count": count
                }
                for cat, total, count in expenses_by_category
            ]
        }

    @staticmethod
    def get_recent_activity(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent financial activity"""
        recent_records = db.query(FinancialRecord).order_by(
            FinancialRecord.date.desc(),
            FinancialRecord.created_at.desc()
        ).limit(limit).all()

        return [
            {
                "id": record.id,
                "amount": float(record.amount),
                "type": record.type.value,
                "category": record.category,
                "date": record.date.isoformat(),
                "description": record.description,
                "created_at": record.created_at.isoformat()
            }
            for record in recent_records
        ]

    @staticmethod
    def get_monthly_trends(db: Session, months: int = 6) -> Dict[str, Any]:
        """Get monthly financial trends"""
        # Calculate date range
        end_date = date.today()
        start_date = end_date - timedelta(days=months * 30)

        # Query monthly data
        monthly_data = db.query(
            extract('year', FinancialRecord.date).label('year'),
            extract('month', FinancialRecord.date).label('month'),
            FinancialRecord.type,
            func.sum(FinancialRecord.amount).label('total')
        ).filter(
            FinancialRecord.date >= start_date
        ).group_by(
            'year', 'month', FinancialRecord.type
        ).order_by('year', 'month').all()

        # Format data
        trends = {}
        for year, month, record_type, total in monthly_data:
            month_key = f"{int(year)}-{int(month):02d}"
            if month_key not in trends:
                trends[month_key] = {
                    "month": month_key,
                    "income": 0.0,
                    "expenses": 0.0,
                    "net": 0.0
                }
            
            if record_type == RecordType.INCOME:
                trends[month_key]["income"] = float(total)
            else:
                trends[month_key]["expenses"] = float(total)
            
            trends[month_key]["net"] = trends[month_key]["income"] - trends[month_key]["expenses"]

        return {
            "trends": list(trends.values())
        }

    @staticmethod
    def get_weekly_summary(db: Session, weeks: int = 4) -> Dict[str, Any]:
        """Get weekly financial summary"""
        end_date = date.today()
        start_date = end_date - timedelta(weeks=weeks)

        weekly_income = db.query(func.sum(FinancialRecord.amount)).filter(
            FinancialRecord.type == RecordType.INCOME,
            FinancialRecord.date >= start_date
        ).scalar() or Decimal('0')

        weekly_expenses = db.query(func.sum(FinancialRecord.amount)).filter(
            FinancialRecord.type == RecordType.EXPENSE,
            FinancialRecord.date >= start_date
        ).scalar() or Decimal('0')

        return {
            "period": f"Last {weeks} weeks",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_income": float(weekly_income),
            "total_expenses": float(weekly_expenses),
            "net_balance": float(weekly_income - weekly_expenses)
        }
