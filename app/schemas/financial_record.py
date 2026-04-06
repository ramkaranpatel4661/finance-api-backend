from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from app.models.financial_record import RecordType


class FinancialRecordBase(BaseModel):
    amount: Decimal = Field(..., gt=0)
    type: RecordType
    category: str = Field(..., min_length=1, max_length=100)
    date: date
    description: Optional[str] = Field(None, max_length=1000)

    @field_validator('amount')
    @classmethod
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        # Round to 2 decimal places
        return round(v, 2)


class FinancialRecordCreate(FinancialRecordBase):
    pass


class FinancialRecordUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    type: Optional[RecordType] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    date: Optional[date] = None
    description: Optional[str] = Field(None, max_length=1000)

    @field_validator('amount')
    @classmethod
    def round_amount(cls, v):
        if v is not None:
            return round(v, 2)
        return v


class FinancialRecordResponse(FinancialRecordBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FinancialRecordFilter(BaseModel):
    type: Optional[RecordType] = None
    category: Optional[str] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    min_amount: Optional[Decimal] = None
    max_amount: Optional[Decimal] = None
