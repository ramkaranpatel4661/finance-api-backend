# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
Include `X-User-Id` header in all authenticated requests:
```
X-User-Id: 1
```

---

## Authentication Endpoints

### POST /api/auth/login
Login and get user credentials

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user_id": 1,
  "username": "admin",
  "role": "admin",
  "instruction": "Use the user_id in X-User-Id header for subsequent requests"
}
```

### POST /api/auth/logout
Logout current user

**Headers:** `X-User-Id: 1`

**Response:**
```json
{
  "message": "Logout successful"
}
```

### GET /api/auth/me
Get current user information

**Headers:** `X-User-Id: 1`

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@finance.com",
  "role": "admin",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

## User Management (Admin Only)

### POST /api/users
Create a new user

**Headers:** `X-User-Id: 1`

**Request:**
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "securepass123",
  "role": "analyst",
  "is_active": true
}
```

**Response:** User object (same as GET /api/users/{id})

### GET /api/users
List all users

**Headers:** `X-User-Id: 1`

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@finance.com",
    "role": "admin",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

### GET /api/users/{user_id}
Get user by ID

**Headers:** `X-User-Id: 1`

**Response:** User object

### PUT /api/users/{user_id}
Update user information

**Headers:** `X-User-Id: 1`

**Request:**
```json
{
  "email": "updated@example.com",
  "role": "analyst",
  "is_active": false,
  "password": "newpassword123"
}
```
*All fields are optional*

**Response:** Updated user object

### DELETE /api/users/{user_id}
Deactivate user

**Headers:** `X-User-Id: 1`

**Response:** 204 No Content

### PUT /api/users/{user_id}/role
Update user role

**Headers:** `X-User-Id: 1`

**Request:**
```json
"analyst"
```
*Valid values: "viewer", "analyst", "admin"*

**Response:** Updated user object

---

## Financial Records

### POST /api/records
Create a new financial record

**Headers:** `X-User-Id: 1` (Analyst or Admin)

**Request:**
```json
{
  "amount": 1500.50,
  "type": "income",
  "category": "Salary",
  "date": "2024-01-15",
  "description": "Monthly salary payment"
}
```

**Fields:**
- `amount`: Positive decimal (required)
- `type`: "income" or "expense" (required)
- `category`: String, 1-100 characters (required)
- `date`: ISO date format YYYY-MM-DD (required)
- `description`: String, max 1000 characters (optional)

**Response:**
```json
{
  "id": 1,
  "amount": 1500.50,
  "type": "income",
  "category": "Salary",
  "date": "2024-01-15",
  "description": "Monthly salary payment",
  "user_id": 1,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### GET /api/records
List financial records with filters

**Headers:** `X-User-Id: 1` (All roles)

**Query Parameters:**
- `skip`: Number to skip (default: 0)
- `limit`: Max to return (default: 100, max: 1000)
- `type`: Filter by type ("income" or "expense")
- `category`: Filter by category
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)
- `min_amount`: Minimum amount
- `max_amount`: Maximum amount

**Example:**
```
GET /api/records?type=expense&category=Groceries&date_from=2024-01-01&limit=50
```

**Response:** Array of financial record objects

### GET /api/records/{record_id}
Get financial record by ID

**Headers:** `X-User-Id: 1` (All roles)

**Response:** Financial record object

### PUT /api/records/{record_id}
Update financial record

**Headers:** `X-User-Id: 1` (Admin only)

**Request:**
```json
{
  "amount": 1600.00,
  "type": "income",
  "category": "Salary",
  "date": "2024-01-15",
  "description": "Updated description"
}
```
*All fields are optional*

**Response:** Updated financial record object

### DELETE /api/records/{record_id}
Delete financial record

**Headers:** `X-User-Id: 1` (Admin only)

**Response:** 204 No Content

---

## Dashboard Analytics

### GET /api/dashboard/summary
Get overall financial summary

**Headers:** `X-User-Id: 1` (All roles)

**Response:**
```json
{
  "total_income": 11250.50,
  "total_expenses": 3841.50,
  "net_balance": 7409.00,
  "total_records": 18,
  "income_count": 6,
  "expense_count": 12
}
```

### GET /api/dashboard/by-category
Get category-wise breakdown

**Headers:** `X-User-Id: 1` (All roles)

**Response:**
```json
{
  "income_by_category": [
    {
      "category": "Salary",
      "total": 5000.00,
      "count": 1
    },
    {
      "category": "Freelance",
      "total": 1500.00,
      "count": 1
    }
  ],
  "expenses_by_category": [
    {
      "category": "Rent",
      "total": 1500.00,
      "count": 1
    },
    {
      "category": "Groceries",
      "total": 350.75,
      "count": 1
    }
  ]
}
```

### GET /api/dashboard/recent
Get recent financial activity

**Headers:** `X-User-Id: 1` (All roles)

**Query Parameters:**
- `limit`: Number of recent records (default: 10, max: 50)

**Response:**
```json
{
  "recent_records": [
    {
      "id": 18,
      "amount": 5000.00,
      "type": "income",
      "category": "Salary",
      "date": "2024-01-20",
      "description": "Monthly salary",
      "created_at": "2024-01-20T08:00:00"
    }
  ]
}
```

### GET /api/dashboard/trends
Get monthly financial trends

**Headers:** `X-User-Id: 1` (All roles)

**Query Parameters:**
- `months`: Number of months to analyze (default: 6, max: 24)

**Response:**
```json
{
  "trends": [
    {
      "month": "2024-01",
      "income": 7250.50,
      "expenses": 3841.50,
      "net": 3409.00
    },
    {
      "month": "2023-12",
      "income": 5000.00,
      "expenses": 2500.00,
      "net": 2500.00
    }
  ]
}
```

### GET /api/dashboard/weekly
Get weekly summary

**Headers:** `X-User-Id: 1` (All roles)

**Query Parameters:**
- `weeks`: Number of weeks to analyze (default: 4, max: 52)

**Response:**
```json
{
  "period": "Last 4 weeks",
  "start_date": "2023-12-24",
  "end_date": "2024-01-21",
  "total_income": 7250.50,
  "total_expenses": 3841.50,
  "net_balance": 3409.00
}
```

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `204 No Content`: Successful deletion
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Example Error Responses

**401 Unauthorized:**
```json
{
  "detail": "Authentication required. Please provide X-User-Id header."
}
```

**403 Forbidden:**
```json
{
  "detail": "Admin access required"
}
```

**404 Not Found:**
```json
{
  "detail": "Financial record not found"
}
```

**400 Bad Request:**
```json
{
  "detail": "Username already exists"
}
```

---

## Data Types & Enums

### UserRole Enum
- `viewer`: Read-only access
- `analyst`: Can create records
- `admin`: Full access

### RecordType Enum
- `income`: Income transaction
- `expense`: Expense transaction

### Date Format
ISO 8601: `YYYY-MM-DD` (e.g., "2024-01-15")

### Decimal Precision
Amounts are stored with 2 decimal places (e.g., 1500.50)

---

## Rate Limits
*Not implemented in current version*

## Versioning
Current API version: v1.0.0

---

**For interactive documentation, visit: http://localhost:8000/docs**
