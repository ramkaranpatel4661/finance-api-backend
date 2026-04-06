# Finance Data Processing and Access Control Backend

A comprehensive backend API built with **FastAPI** and **PostgreSQL** for managing financial records with role-based access control. This project demonstrates clean architecture, proper separation of concerns, and industry-standard backend development practices.

## 🎯 Project Overview

This backend system provides a complete solution for a finance dashboard application where different users can interact with financial data based on their assigned roles. The system implements proper authentication, authorization, data validation, and comprehensive analytics endpoints.

### Key Features

- **Role-Based Access Control (RBAC)**: Three distinct user roles with different permission levels
- **Financial Records Management**: Full CRUD operations for income and expense tracking
- **Dashboard Analytics**: Comprehensive financial summaries and trend analysis
- **Data Validation**: Robust input validation using Pydantic models
- **Clean Architecture**: Proper separation of concerns with models, schemas, services, and routers
- **RESTful API Design**: Well-structured endpoints following REST principles
- **PostgreSQL Database**: Reliable data persistence with SQLAlchemy ORM

## 🏗️ Architecture & Design

### Project Structure

```
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # Database configuration and session management
│   ├── models/                 # SQLAlchemy database models
│   │   ├── user.py            # User model with role enum
│   │   └── financial_record.py # Financial record model
│   ├── schemas/                # Pydantic schemas for validation
│   │   ├── user.py            # User request/response schemas
│   │   └── financial_record.py # Financial record schemas
│   ├── routers/                # API route handlers
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── users.py           # User management endpoints
│   │   ├── financial_records.py # Financial records endpoints
│   │   └── dashboard.py        # Analytics and dashboard endpoints
│   ├── services/               # Business logic layer
│   │   ├── user_service.py     # User management operations
│   │   ├── financial_service.py # Financial records operations
│   │   └── dashboard_service.py # Analytics and aggregations
│   ├── middleware/             # Custom middleware
│   │   └── auth_middleware.py  # Authentication and authorization
│   └── utils/                  # Helper functions and utilities
├── requirements.txt            # Python dependencies
├── seed_data.py               # Database seeding script
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

### Technology Stack

- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL with SQLAlchemy 2.0
- **Validation**: Pydantic 2.5
- **Authentication**: Password hashing with bcrypt
- **Server**: Uvicorn (ASGI server)

## 📋 User Roles & Permissions

The system implements three user roles with hierarchical permissions:

### 1. Viewer
- ✅ View all financial records
- ✅ Access dashboard summaries and analytics
- ❌ Cannot create, update, or delete records
- ❌ Cannot manage users

### 2. Analyst
- ✅ All Viewer permissions
- ✅ Create new financial records
- ❌ Cannot update or delete existing records
- ❌ Cannot manage users

### 3. Admin
- ✅ All Analyst permissions
- ✅ Update financial records
- ✅ Delete financial records
- ✅ Full user management (create, update, delete users)
- ✅ Change user roles

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (or extract the project files)
   ```bash
   cd "Zorvyn bakend developer"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```sql
   CREATE DATABASE finance_db;
   CREATE USER finance_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE finance_db TO finance_user;
   ```

5. **Configure environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and update the DATABASE_URL
   # Example: postgresql://finance_user:your_password@localhost:5432/finance_db
   ```

6. **Seed the database** (optional but recommended)
   ```bash
   python seed_data.py
   ```
   
   This creates three sample users:
   - **admin** / admin123 (Admin role)
   - **analyst** / analyst123 (Analyst role)
   - **viewer** / viewer123 (Viewer role)

7. **Start the server**
   ```bash
   python -m app.main
   
   # Or use uvicorn directly
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Authentication

This demo uses a simplified authentication mechanism via headers. In production, this would be replaced with JWT tokens.

**How to authenticate:**

1. Login to get your user ID:
   ```bash
   POST /api/auth/login
   {
     "username": "admin",
     "password": "admin123"
   }
   ```

2. Use the returned `user_id` in subsequent requests:
   ```bash
   # Add this header to all requests
   X-User-Id: 1
   ```

### API Endpoints Overview

#### Authentication
- `POST /api/auth/login` - Login and get user ID
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user info

#### User Management (Admin only)
- `POST /api/users` - Create new user
- `GET /api/users` - List all users
- `GET /api/users/{id}` - Get user details
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Deactivate user
- `PUT /api/users/{id}/role` - Update user role

#### Financial Records
- `POST /api/records` - Create record (Analyst, Admin)
- `GET /api/records` - List records with filters (All roles)
- `GET /api/records/{id}` - Get record details (All roles)
- `PUT /api/records/{id}` - Update record (Admin only)
- `DELETE /api/records/{id}` - Delete record (Admin only)

#### Dashboard Analytics
- `GET /api/dashboard/summary` - Overall financial summary
- `GET /api/dashboard/by-category` - Category-wise breakdown
- `GET /api/dashboard/recent` - Recent activity
- `GET /api/dashboard/trends` - Monthly trends
- `GET /api/dashboard/weekly` - Weekly summary

## 🔍 Example Usage

### 1. Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 2. Create a Financial Record
```bash
curl -X POST "http://localhost:8000/api/records" \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 1" \
  -d '{
    "amount": 1500.50,
    "type": "income",
    "category": "Salary",
    "date": "2024-01-15",
    "description": "Monthly salary payment"
  }'
```

### 3. Get Dashboard Summary
```bash
curl -X GET "http://localhost:8000/api/dashboard/summary" \
  -H "X-User-Id: 1"
```

### 4. List Records with Filters
```bash
curl -X GET "http://localhost:8000/api/records?type=expense&category=Groceries&date_from=2024-01-01" \
  -H "X-User-Id: 1"
```

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Bcrypt hashed password
- `role`: Enum (viewer, analyst, admin)
- `is_active`: Boolean flag
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Financial Records Table
- `id`: Primary key
- `amount`: Decimal(12, 2)
- `type`: Enum (income, expense)
- `category`: String
- `date`: Date
- `description`: Text (optional)
- `user_id`: Foreign key to users
- `created_at`: Timestamp
- `updated_at`: Timestamp

## 🛡️ Security Features

1. **Password Hashing**: All passwords are hashed using bcrypt
2. **Role-Based Access Control**: Endpoints protected by role requirements
3. **Input Validation**: Pydantic models validate all input data
4. **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
5. **Error Handling**: Comprehensive error handling with appropriate status codes

## ✨ Design Decisions & Assumptions

### Assumptions Made

1. **Authentication**: Using simple header-based auth for demo purposes. In production, implement JWT tokens.
2. **Single Tenant**: No multi-organization support; all users share the same data pool.
3. **Currency**: All amounts assumed to be in USD.
4. **Categories**: Free-form category strings rather than predefined options.
5. **Soft Delete**: Users are deactivated rather than hard-deleted; records are hard-deleted.
6. **Date Handling**: All dates use ISO 8601 format (YYYY-MM-DD).

### Why These Technologies?

- **FastAPI**: Modern, fast, automatic API documentation, excellent async support
- **PostgreSQL**: Robust, reliable, excellent for financial data, ACID compliance
- **SQLAlchemy**: Mature ORM with great features and performance
- **Pydantic**: Powerful data validation with minimal boilerplate
- **Bcrypt**: Industry-standard password hashing

### Architecture Choices

1. **Service Layer**: Business logic separated from route handlers for testability
2. **Dependency Injection**: FastAPI's DI system used for database sessions and auth
3. **Repository Pattern**: Services encapsulate database operations
4. **Schema Separation**: Clear distinction between database models and API schemas

## 🧪 Testing

To test the API manually:

1. Start the server
2. Open http://localhost:8000/docs (Swagger UI)
3. Use the "Authorize" button or add `X-User-Id` header manually
4. Try different endpoints with different user roles

### Test Scenarios

**As Admin:**
- Create users, records
- Update and delete records
- Access all dashboard features

**As Analyst:**
- Create financial records
- View all records and dashboards
- Cannot update/delete records or manage users

**As Viewer:**
- View records and dashboards only
- Cannot create, update, or delete anything

## 🚧 Future Enhancements

If this were a production system, consider adding:

- JWT-based authentication
- Pagination for all list endpoints
- Search functionality
- Export to CSV/Excel
- Email notifications
- Audit logging
- Rate limiting
- Unit and integration tests
- API versioning
- Soft delete for records
- Multi-currency support
- Scheduled reports

## 📝 Notes

- This is a demonstration project for backend assessment
- Focus is on clean code, proper architecture, and maintainability
- Security features are simplified for demo purposes
- In production, implement proper JWT authentication, rate limiting, and monitoring

## 🤝 API Response Format

All responses follow a consistent format:

**Success Response:**
```json
{
  "id": 1,
  "field1": "value1",
  "field2": "value2"
}
```

**Error Response:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

## 📞 Support

For issues or questions:
1. Check the API documentation at `/docs`
2. Review this README
3. Check database configuration in `.env`

---

**Built with ❤️ using FastAPI and PostgreSQL**
