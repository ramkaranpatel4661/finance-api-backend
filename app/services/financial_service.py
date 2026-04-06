from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date
from app.models.financial_record import FinancialRecord, RecordType
from app.schemas.financial_record import FinancialRecordCreate, FinancialRecordUpdate, FinancialRecordFilter


class FinancialRecordService:
    """Service class for financial record operations"""

    @staticmethod
    def create_record(db: Session, record_data: FinancialRecordCreate, user_id: int) -> FinancialRecord:
        """Create a new financial record"""
        record = FinancialRecord(
            amount=record_data.amount,
            type=record_data.type,
            category=record_data.category,
            date=record_data.date,
            description=record_data.description,
            user_id=user_id
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_record_by_id(db: Session, record_id: int) -> Optional[FinancialRecord]:
        """Get financial record by ID"""
        return db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()

    @staticmethod
    def get_all_records(
        db: Session,
        filters: Optional[FinancialRecordFilter] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[FinancialRecord]:
        """Get all financial records with optional filters"""
        query = db.query(FinancialRecord)

        if filters:
            if filters.type:
                query = query.filter(FinancialRecord.type == filters.type)
            if filters.category:
                query = query.filter(FinancialRecord.category == filters.category)
            if filters.date_from:
                query = query.filter(FinancialRecord.date >= filters.date_from)
            if filters.date_to:
                query = query.filter(FinancialRecord.date <= filters.date_to)
            if filters.min_amount:
                query = query.filter(FinancialRecord.amount >= filters.min_amount)
            if filters.max_amount:
                query = query.filter(FinancialRecord.amount <= filters.max_amount)

        return query.order_by(FinancialRecord.date.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def update_record(db: Session, record_id: int, record_data: FinancialRecordUpdate) -> FinancialRecord:
        """Update financial record"""
        record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Financial record not found"
            )

        update_data = record_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(record, field, value)

        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def delete_record(db: Session, record_id: int) -> bool:
        """Delete financial record"""
        record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Financial record not found"
            )
        
        db.delete(record)
        db.commit()
        return True

    @staticmethod
    def get_records_by_category(db: Session, category: str) -> List[FinancialRecord]:
        """Get all records for a specific category"""
        return db.query(FinancialRecord).filter(FinancialRecord.category == category).all()

    @staticmethod
    def get_records_by_date_range(
        db: Session,
        start_date: date,
        end_date: date
    ) -> List[FinancialRecord]:
        """Get records within a date range"""
        return db.query(FinancialRecord).filter(
            and_(
                FinancialRecord.date >= start_date,
                FinancialRecord.date <= end_date
            )
        ).order_by(FinancialRecord.date.desc()).all()
