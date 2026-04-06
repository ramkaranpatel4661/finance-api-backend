# Getting Started - Finance Data Processing Backend

## Welcome! 👋

This guide will help you set up and run the Finance Data Processing Backend in just a few minutes.

## Prerequisites

Before you begin, make sure you have:
- **Python 3.8+** installed ([Download here](https://www.python.org/downloads/))
- **PostgreSQL 12+** installed ([Download here](https://www.postgresql.org/download/))
- **pip** (comes with Python)
- A terminal/command prompt

## Setup Steps

### Step 1: Install Python Dependencies

Open a terminal in the project directory and run:

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Set Up PostgreSQL Database

1. **Start PostgreSQL** (if not already running)

2. **Create the database**:
   ```sql
   -- Open PostgreSQL command line (psql) or use pgAdmin
   CREATE DATABASE finance_db;
   ```

3. **Create a user** (optional, can use existing user):
   ```sql
   CREATE USER finance_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE finance_db TO finance_user;
   ```

### Step 3: Configure Environment Variables

1. **Copy the example environment file**:
   ```bash
   # On Windows
   copy .env.example .env
   
   # On macOS/Linux
   cp .env.example .env
   ```

2. **Edit the `.env` file** with your database credentials:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/finance_db
   DEBUG=True
   HOST=0.0.0.0
   PORT=8000
   ```

   Replace:
   - `username` with your PostgreSQL username (default: `postgres`)
   - `password` with your PostgreSQL password
   - `localhost` with your database host if different
   - `finance_db` with your database name if different

### Step 4: Seed the Database (Recommended)

This creates sample users and financial records for testing:

```bash
python seed_data.py
```

**Sample users created:**
- **Username**: `admin` | **Password**: `admin123` | **Role**: Admin
- **Username**: `analyst` | **Password**: `analyst123` | **Role**: Analyst  
- **Username**: `viewer` | **Password**: `viewer123` | **Role**: Viewer

### Step 5: Start the Server

```bash
python -m app.main
```

Or alternatively:
```bash
uvicorn app.main:app --reload
```

You should see output like:
```
INFO:     Started server process
INFO:     Waiting for application startup.
Database initialized successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 6: Access the API

**Open your browser and go to:**
- **Swagger UI (Interactive API Docs)**: http://localhost:8000/docs
- **ReDoc (Alternative Docs)**: http://localhost:8000/redoc
- **API Base URL**: http://localhost:8000/api

## Quick Test

Let's test the API to make sure everything works!

### Using Swagger UI (Easiest)

1. Open http://localhost:8000/docs
2. Find **"POST /api/auth/login"**
3. Click **"Try it out"**
4. Enter:
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
5. Click **"Execute"**
6. Copy the `user_id` from the response (should be `1`)
7. For any other endpoint, click "Try it out" and enter `1` in the `X-User-Id` parameter

### Using Command Line (cURL)

```bash
# Test login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Get dashboard summary (use user_id from login)
curl -X GET "http://localhost:8000/api/dashboard/summary" \
  -H "X-User-Id: 1"

# Create a financial record
curl -X POST "http://localhost:8000/api/records" \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 1" \
  -d '{
    "amount": 1000.00,
    "type": "income",
    "category": "Salary",
    "date": "2024-01-20",
    "description": "Monthly salary"
  }'

# List all records
curl -X GET "http://localhost:8000/api/records" \
  -H "X-User-Id: 1"
```

## Troubleshooting

### Error: "Database connection failed"

**Problem**: Can't connect to PostgreSQL

**Solutions**:
- Make sure PostgreSQL is running
- Check your `DATABASE_URL` in `.env`
- Verify username and password are correct
- Ensure the database `finance_db` exists

### Error: "Module not found"

**Problem**: Python packages not installed

**Solution**:
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install packages
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"

**Problem**: Another application is using port 8000

**Solution**:
Either stop the other application, or change the port in `.env`:
```env
PORT=8001
```

### Error: "Authentication required"

**Problem**: Missing X-User-Id header

**Solution**:
Always include the `X-User-Id` header after logging in:
```bash
-H "X-User-Id: 1"
```

### Database Tables Not Created

**Problem**: Tables don't exist in database

**Solution**:
The tables are automatically created when you start the server. If they're not:
1. Stop the server
2. Drop the database and recreate it
3. Start the server again

## Project Structure

```
├── app/                    # Main application package
│   ├── main.py            # Application entry point
│   ├── database.py        # Database configuration
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic validation schemas
│   ├── routers/           # API endpoints
│   ├── services/          # Business logic
│   └── middleware/        # Authentication & authorization
├── seed_data.py           # Database seeding script
├── requirements.txt       # Python dependencies
└── Documentation/
    ├── README.md          # Main documentation
    ├── QUICKSTART.md      # Quick start guide
    ├── API_DOCS.md        # API documentation
    └── ARCHITECTURE.md    # Architecture details
```

## Next Steps

Now that you have the API running:

1. **Explore the API**: Open http://localhost:8000/docs and try different endpoints

2. **Test Different Roles**:
   - Login as `viewer` - Can only read data
   - Login as `analyst` - Can read and create records
   - Login as `admin` - Full access to everything

3. **Read the Documentation**:
   - **API_DOCS.md** - Complete API reference
   - **ARCHITECTURE.md** - Technical architecture details
   - **README.md** - Comprehensive project overview

4. **Add Your Own Data**: Create your own users and financial records

5. **Explore Dashboard Features**: Check out the analytics endpoints:
   - `/api/dashboard/summary` - Overall financial summary
   - `/api/dashboard/by-category` - Category breakdowns
   - `/api/dashboard/trends` - Monthly trends
   - `/api/dashboard/recent` - Recent activity

## Example Workflow

Here's a typical workflow to test all features:

```bash
# 1. Login as admin
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
# Note the user_id from response

# 2. Create a new user
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 1" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "secure123",
    "role": "analyst"
  }'

# 3. Add income record
curl -X POST "http://localhost:8000/api/records" \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 1" \
  -d '{
    "amount": 5000.00,
    "type": "income",
    "category": "Salary",
    "date": "2024-01-01"
  }'

# 4. Add expense record
curl -X POST "http://localhost:8000/api/records" \
  -H "Content-Type: application/json" \
  -H "X-User-Id: 1" \
  -d '{
    "amount": 1500.00,
    "type": "expense",
    "category": "Rent",
    "date": "2024-01-05"
  }'

# 5. View dashboard
curl -X GET "http://localhost:8000/api/dashboard/summary" \
  -H "X-User-Id: 1"

# 6. Get category breakdown
curl -X GET "http://localhost:8000/api/dashboard/by-category" \
  -H "X-User-Id: 1"
```

## Support & Help

If you encounter any issues:

1. Check this guide for common problems
2. Review the **README.md** for detailed information
3. Check the **API_DOCS.md** for API usage
4. Look at **ARCHITECTURE.md** for technical details

## Ready to Build!

You're all set! The API is running and ready to use. Start exploring the endpoints and building your finance dashboard application.

**Happy coding! 🚀**
