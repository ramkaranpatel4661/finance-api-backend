from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum as SQLEnum, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class RecordType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(precision=12, scale=2), nullable=False)
    type = Column(SQLEnum(RecordType), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="financial_records")

    def __repr__(self):
        return f"<FinancialRecord(id={self.id}, type='{self.type}', amount={self.amount}, category='{self.category}')>"
