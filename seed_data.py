"""
Seed script to populate the database with sample data
Run this after setting up the database to get started quickly
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models.user import User, UserRole
from app.models.financial_record import FinancialRecord, RecordType
from datetime import date, timedelta
from decimal import Decimal


def create_sample_users(db: Session):
    """Create sample users with different roles"""
    users = []
    
    # Admin user
    admin = User(
        username="admin",
        email="admin@finance.com",
        role=UserRole.ADMIN,
        is_active=True
    )
    admin.set_password("admin123")
    users.append(admin)
    
    # Analyst user
    analyst = User(
        username="analyst",
        email="analyst@finance.com",
        role=UserRole.ANALYST,
        is_active=True
    )
    analyst.set_password("analyst123")
    users.append(analyst)
    
    # Viewer user
    viewer = User(
        username="viewer",
        email="viewer@finance.com",
        role=UserRole.VIEWER,
        is_active=True
    )
    viewer.set_password("viewer123")
    users.append(viewer)
    
    db.add_all(users)
    db.commit()
    
    print("✓ Created sample users:")
    print("  - admin (password: admin123) - Role: ADMIN")
    print("  - analyst (password: analyst123) - Role: ANALYST")
    print("  - viewer (password: viewer123) - Role: VIEWER")
    
    return users


def create_sample_records(db: Session, user_id: int):
    """Create sample financial records"""
    records = []
    today = date.today()
    
    # Sample income records
    income_data = [
        ("Salary", Decimal("5000.00"), 0),
        ("Freelance", Decimal("1500.00"), 5),
        ("Investment Returns", Decimal("750.50"), 10),
        ("Bonus", Decimal("2000.00"), 15),
        ("Consulting", Decimal("1200.00"), 20),
        ("Side Project", Decimal("800.00"), 25),
    ]
    
    for category, amount, days_ago in income_data:
        record = FinancialRecord(
            amount=amount,
            type=RecordType.INCOME,
            category=category,
            date=today - timedelta(days=days_ago),
            description=f"Sample {category.lower()} record",
            user_id=user_id
        )
        records.append(record)
    
    # Sample expense records
    expense_data = [
        ("Rent", Decimal("1500.00"), 1),
        ("Groceries", Decimal("350.75"), 3),
        ("Utilities", Decimal("200.00"), 4),
        ("Transportation", Decimal("150.50"), 7),
        ("Entertainment", Decimal("120.00"), 8),
        ("Healthcare", Decimal("300.00"), 12),
        ("Shopping", Decimal("450.25"), 14),
        ("Dining Out", Decimal("180.00"), 18),
        ("Internet", Decimal("60.00"), 22),
        ("Phone Bill", Decimal("50.00"), 24),
        ("Insurance", Decimal("400.00"), 28),
        ("Gym Membership", Decimal("80.00"), 30),
    ]
    
    for category, amount, days_ago in expense_data:
        record = FinancialRecord(
            amount=amount,
            type=RecordType.EXPENSE,
            category=category,
            date=today - timedelta(days=days_ago),
            description=f"Sample {category.lower()} expense",
            user_id=user_id
        )
        records.append(record)
    
    db.add_all(records)
    db.commit()
    
    print(f"✓ Created {len(records)} sample financial records")
    print(f"  - {len(income_data)} income records")
    print(f"  - {len(expense_data)} expense records")


def seed_database():
    """Main function to seed the database"""
    print("Starting database seeding...")
    print("-" * 50)
    
    # Initialize database
    init_db()
    print("✓ Database tables initialized")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("\n⚠ Database already contains data!")
            response = input("Do you want to continue and add more sample data? (y/n): ")
            if response.lower() != 'y':
                print("Seeding cancelled.")
                return
        
        # Create sample users
        users = create_sample_users(db)
        
        # Create sample records for the admin user
        create_sample_records(db, users[0].id)
        
        print("-" * 50)
        print("✓ Database seeding completed successfully!")
        print("\nYou can now start the API server and login with:")
        print("  Username: admin, Password: admin123")
        print("  Username: analyst, Password: analyst123")
        print("  Username: viewer, Password: viewer123")
        
    except Exception as e:
        print(f"\n✗ Error during seeding: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
