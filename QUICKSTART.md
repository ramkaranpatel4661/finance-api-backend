# Quick Start Guide

## Fastest Way to Get Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database
Create a PostgreSQL database named `finance_db`:
```sql
CREATE DATABASE finance_db;
```

### 3. Configure Environment
Create a `.env` file (copy from `.env.example`):
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/finance_db
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### 4. Seed Sample Data
```bash
python seed_data.py
```

This creates three users:
- **Username**: `admin` | **Password**: `admin123` | **Role**: Admin
- **Username**: `analyst` | **Password**: `analyst123` | **Role**: Analyst
- **Username**: `viewer` | **Password**: `viewer123` | **Role**: Viewer

### 5. Start the Server
```bash
python -m app.main
```

Or with uvicorn:
```bash
uvicorn app.main:app --reload
```

### 6. Access the API
- **Swagger Documentation**: http://localhost:8000/docs
- **API Base URL**: http://localhost:8000/api

---

## Quick API Testing

### Step 1: Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
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

### Step 2: Get Your Profile
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "X-User-Id: 1"
```

### Step 3: View Dashboard Summary
```bash
curl -X GET "http://localhost:8000/api/dashboard/summary" \
  -H "X-User-Id: 1"
```

### Step 4: Create a Financial Record
```bash
curl -X POST "http://localhost:8000/api/records" \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 1" \
  -d '{
    "amount": 2500.00,
    "type": "income",
    "category": "Freelance Work",
    "date": "2024-01-20",
    "description": "Web development project"
  }'
```

### Step 5: List All Records
```bash
curl -X GET "http://localhost:8000/api/records" \
  -H "X-User-Id: 1"
```

### Step 6: Get Category Breakdown
```bash
curl -X GET "http://localhost:8000/api/dashboard/by-category" \
  -H "X-User-Id: 1"
```

---

## Testing Different Roles

### As Viewer (Read-only)
```bash
# Login as viewer
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "viewer", "password": "viewer123"}'

# Try to create a record (will fail - forbidden)
curl -X POST "http://localhost:8000/api/records" \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 3" \
  -d '{
    "amount": 100.00,
    "type": "expense",
    "category": "Test",
    "date": "2024-01-20"
  }'

# View records (will succeed)
curl -X GET "http://localhost:8000/api/records" \
  -H "X-User-Id: 3"
```

### As Analyst (Can create, not update/delete)
```bash
# Login as analyst
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "analyst", "password": "analyst123"}'

# Create a record (will succeed)
curl -X POST "http://localhost:8000/api/records" \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 2" \
  -d '{
    "amount": 500.00,
    "type": "income",
    "category": "Consulting",
    "date": "2024-01-20"
  }'

# Try to delete a record (will fail - forbidden)
curl -X DELETE "http://localhost:8000/api/records/1" \
  -H "X-User-Id: 2"
```

### As Admin (Full access)
```bash
# Login as admin
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Update a record (will succeed)
curl -X PUT "http://localhost:8000/api/records/1" \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 1" \
  -d '{
    "amount": 5500.00,
    "description": "Updated salary amount"
  }'

# Create a new user (will succeed)
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 1" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "role": "analyst"
  }'
```

---

## Common Issues & Solutions

### Issue: "Database connection failed"
**Solution**: Ensure PostgreSQL is running and DATABASE_URL in .env is correct

### Issue: "Module not found"
**Solution**: Activate virtual environment and install requirements:
```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Issue: "Port already in use"
**Solution**: Change PORT in .env or stop the other process using port 8000

### Issue: "Authentication required"
**Solution**: Always include `X-User-Id` header in requests after logging in

---

## Next Steps

1. **Explore the API**: Open http://localhost:8000/docs and try different endpoints
2. **Test Role Permissions**: Login as different users and observe access restrictions
3. **Add Your Data**: Create your own financial records
4. **View Analytics**: Check dashboard endpoints for insights

---

## Using Swagger UI (Easiest Method)

1. Open http://localhost:8000/docs
2. Find the "POST /api/auth/login" endpoint
3. Click "Try it out"
4. Enter credentials (admin/admin123)
5. Note the `user_id` from response
6. For subsequent requests:
   - Click on any endpoint
   - Click "Try it out"
   - Scroll to "Parameters"
   - Enter the user_id in the `X-User-Id` field
   - Fill in request body if needed
   - Click "Execute"

This is the easiest way to test the API without using command line!

---

**Ready to go! 🚀**
