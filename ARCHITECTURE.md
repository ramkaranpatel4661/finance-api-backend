# Architecture & Design Decisions

## System Architecture

### High-Level Architecture

```
┌─────────────────┐
│   Client/UI     │
│  (Frontend App) │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────────────────────────┐
│         FastAPI Application         │
│                                     │
│  ┌──────────────────────────────┐  │
│  │      API Layer (Routers)     │  │
│  │  - auth.py                   │  │
│  │  - users.py                  │  │
│  │  - financial_records.py      │  │
│  │  - dashboard.py              │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│  ┌──────────▼───────────────────┐  │
│  │   Middleware (Auth/RBAC)     │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│  ┌──────────▼───────────────────┐  │
│  │   Business Logic (Services)  │  │
│  │  - user_service.py           │  │
│  │  - financial_service.py      │  │
│  │  - dashboard_service.py      │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│  ┌──────────▼───────────────────┐  │
│  │  Validation (Pydantic)       │  │
│  │  - Schemas                   │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│  ┌──────────▼───────────────────┐  │
│  │   Data Layer (SQLAlchemy)    │  │
│  │  - Models                    │  │
│  └──────────┬───────────────────┘  │
└─────────────┼───────────────────────┘
              │ SQL
              ▼
    ┌─────────────────┐
    │   PostgreSQL    │
    │    Database     │
    └─────────────────┘
```

### Layer Responsibilities

1. **API Layer (Routers)**
   - HTTP endpoint definitions
   - Request/response handling
   - Route organization
   - Dependency injection setup

2. **Middleware Layer**
   - Authentication verification
   - Authorization (role-based access control)
   - Request validation
   - Error handling

3. **Service Layer**
   - Business logic implementation
   - Data orchestration
   - Complex operations
   - Transaction management

4. **Validation Layer (Schemas)**
   - Input validation
   - Output serialization
   - Type checking
   - Data transformation

5. **Data Layer (Models)**
   - Database schema definition
   - ORM mappings
   - Relationships
   - Database operations

---

## Design Patterns

### 1. Layered Architecture
The application follows a strict layered architecture:
- **Presentation** → **Business Logic** → **Data Access** → **Database**

**Benefits:**
- Clear separation of concerns
- Easier testing and maintenance
- Independent layer modifications
- Reduced coupling

### 2. Dependency Injection
FastAPI's built-in DI system manages dependencies:
```python
def get_current_user(
    x_user_id: Optional[int] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    # Authentication logic
```

**Benefits:**
- Loose coupling
- Easy to mock for testing
- Clear dependency graph
- Automatic resource management

### 3. Repository Pattern (via Services)
Services act as repositories, encapsulating data access:
```python
class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        # Implementation
```

**Benefits:**
- Centralized data access logic
- Easier to swap data sources
- Consistent error handling
- Reusable business logic

### 4. DTO Pattern (Data Transfer Objects)
Pydantic schemas serve as DTOs:
```python
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
```

**Benefits:**
- Type safety
- Automatic validation
- Clear API contracts
- Prevents over-posting

---

## Security Design

### Authentication Flow

```
1. User sends credentials → POST /api/auth/login
2. Server validates username/password
3. Server returns user_id
4. Client includes X-User-Id in subsequent requests
5. Middleware validates user_id and retrieves user
6. Request proceeds if user is valid and active
```

**Note:** In production, replace with JWT tokens:
```
1. User sends credentials
2. Server returns JWT token
3. Client includes token in Authorization header
4. Middleware validates token signature and expiry
5. Request proceeds if token is valid
```

### Authorization (RBAC)

```python
# Role hierarchy
Viewer < Analyst < Admin

# Permission matrix:
┌──────────────────┬────────┬─────────┬───────┐
│ Action           │ Viewer │ Analyst │ Admin │
├──────────────────┼────────┼─────────┼───────┤
│ View Records     │   ✓    │    ✓    │   ✓   │
│ Create Records   │   ✗    │    ✓    │   ✓   │
│ Update Records   │   ✗    │    ✗    │   ✓   │
│ Delete Records   │   ✗    │    ✗    │   ✓   │
│ Manage Users     │   ✗    │    ✗    │   ✓   │
└──────────────────┴────────┴─────────┴───────┘
```

Implementation:
```python
@router.post("/records")
def create_record(
    current_user: User = Depends(get_current_user)
):
    if current_user.role == UserRole.VIEWER:
        raise HTTPException(403, "Forbidden")
    # Proceed with creation
```

### Password Security

```python
# Password hashing with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"])

# Hashing
password_hash = pwd_context.hash(plain_password)

# Verification
is_valid = pwd_context.verify(plain_password, password_hash)
```

**Security features:**
- Bcrypt with automatic salting
- Configurable work factor
- Resistant to rainbow tables
- Industry-standard implementation

---

## Database Design

### Schema Design Principles

1. **Normalization**: Tables are normalized to 3NF
2. **Foreign Keys**: Enforce referential integrity
3. **Indexes**: On commonly queried fields (username, email, date, category)
4. **Timestamps**: Track creation and modification times
5. **Enums**: Use database-level enums for type safety

### Relationships

```
┌─────────────────┐         ┌─────────────────────┐
│     Users       │         │  Financial Records  │
├─────────────────┤         ├─────────────────────┤
│ id (PK)         │◄───┐    │ id (PK)             │
│ username        │    │    │ amount              │
│ email           │    │    │ type                │
│ password_hash   │    │    │ category            │
│ role            │    │    │ date                │
│ is_active       │    │    │ description         │
│ created_at      │    └────┤ user_id (FK)        │
│ updated_at      │         │ created_at          │
└─────────────────┘         │ updated_at          │
                            └─────────────────────┘
        One-to-Many Relationship
```

### Indexing Strategy

```sql
-- Primary keys (automatically indexed)
users.id
financial_records.id

-- Unique constraints (indexed)
users.username
users.email

-- Foreign keys
financial_records.user_id

-- Query optimization indexes
financial_records.date
financial_records.category
financial_records.type
```

---

## API Design Principles

### RESTful Design

```
Resource-based URLs:
✓ GET    /api/records          (List resources)
✓ POST   /api/records          (Create resource)
✓ GET    /api/records/{id}     (Get single resource)
✓ PUT    /api/records/{id}     (Update resource)
✓ DELETE /api/records/{id}     (Delete resource)

✗ GET    /api/getRecords       (Non-RESTful)
✗ POST   /api/createRecord     (Non-RESTful)
```

### HTTP Status Codes

```
200 OK              - Successful GET/PUT
201 Created         - Successful POST
204 No Content      - Successful DELETE
400 Bad Request     - Invalid input
401 Unauthorized    - Not authenticated
403 Forbidden       - Not authorized
404 Not Found       - Resource doesn't exist
500 Server Error    - Internal error
```

### Consistent Response Format

**Success (Single Resource):**
```json
{
  "id": 1,
  "field1": "value1",
  "field2": "value2"
}
```

**Success (Collection):**
```json
[
  { "id": 1, "field": "value" },
  { "id": 2, "field": "value" }
]
```

**Error:**
```json
{
  "detail": "Error message"
}
```

---

## Data Validation Strategy

### Input Validation (Pydantic)

```python
class FinancialRecordCreate(BaseModel):
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    type: RecordType
    category: str = Field(..., min_length=1, max_length=100)
    date: date
    description: Optional[str] = Field(None, max_length=1000)

    @field_validator('amount')
    @classmethod
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v
```

**Validation levels:**
1. Type validation (automatic)
2. Constraint validation (Field parameters)
3. Custom validators (field_validator)
4. Business rule validation (service layer)

### Error Handling Strategy

```python
try:
    # Database operation
    db.commit()
except IntegrityError as e:
    db.rollback()
    if "username" in str(e.orig):
        raise HTTPException(400, "Username already exists")
    elif "email" in str(e.orig):
        raise HTTPException(400, "Email already exists")
    raise HTTPException(400, "Could not create user")
```

**Error handling levels:**
1. Input validation (Pydantic)
2. Database constraints (SQLAlchemy)
3. Business logic errors (Service layer)
4. HTTP exceptions (Route handlers)
5. Global exception handler (FastAPI)

---

## Performance Considerations

### Database Optimization

1. **Query Optimization**
   - Use `.filter()` for indexed columns
   - Lazy loading for relationships
   - Pagination for large result sets

2. **Connection Pooling**
   - SQLAlchemy manages connection pool
   - Configurable pool size
   - Automatic connection recycling

3. **Indexing**
   - Primary keys, foreign keys
   - Frequently queried fields
   - Unique constraints

### API Optimization

1. **Pagination**
   ```python
   @router.get("/records")
   def list_records(
       skip: int = 0,
       limit: int = 100
   ):
       return service.get_all_records(skip=skip, limit=limit)
   ```

2. **Filtering**
   - Server-side filtering reduces data transfer
   - Query parameters for flexible filtering
   - Indexed fields for fast filtering

3. **Async Support** (Future Enhancement)
   ```python
   # FastAPI supports async
   @router.get("/records")
   async def list_records():
       return await service.get_all_records()
   ```

---

## Scalability Considerations

### Current Architecture (Single Server)

```
Client → FastAPI Server → PostgreSQL Database
```

### Horizontal Scaling (Future)

```
                   ┌─→ FastAPI Server 1 ┐
Client → Load Balancer ──→ FastAPI Server 2 ──→ PostgreSQL (Primary)
                   └─→ FastAPI Server 3 ┘           ↓
                                              PostgreSQL (Replica)
```

**Required changes:**
- Stateless authentication (JWT)
- Session management (Redis)
- Database read replicas
- Caching layer (Redis/Memcached)

### Caching Strategy (Future)

```python
# Cache dashboard summaries
@cache(ttl=300)  # 5 minutes
def get_dashboard_summary():
    return DashboardService.get_overall_summary()

# Cache category breakdown
@cache(ttl=600)  # 10 minutes
def get_category_breakdown():
    return DashboardService.get_category_summary()
```

---

## Testing Strategy

### Unit Tests
```python
def test_create_user():
    user_data = UserCreate(
        username="test",
        email="test@example.com",
        password="password123"
    )
    user = UserService.create_user(db, user_data)
    assert user.username == "test"
    assert user.verify_password("password123")
```

### Integration Tests
```python
def test_create_record_endpoint():
    response = client.post(
        "/api/records",
        headers={"X-User-Id": "1"},
        json={
            "amount": 100.00,
            "type": "income",
            "category": "Test",
            "date": "2024-01-01"
        }
    )
    assert response.status_code == 201
```

### Test Coverage Goals
- Services: 90%+
- Routers: 80%+
- Models: 70%+

---

## Assumptions & Trade-offs

### Assumptions

1. **Single Tenant**: No multi-organization support
2. **USD Currency**: All amounts in one currency
3. **Simple Auth**: Header-based for demo (would use JWT in production)
4. **Hard Delete**: Records permanently deleted (could implement soft delete)
5. **No Audit Trail**: No change history tracking (could add audit logs)

### Trade-offs

| Decision | Benefit | Trade-off |
|----------|---------|-----------|
| PostgreSQL over SQLite | Production-ready, ACID compliance | Requires separate server |
| Synchronous over Async | Simpler code, easier debugging | Lower throughput potential |
| Header auth over JWT | Simpler implementation | Less secure, not production-ready |
| Hard delete over soft | Simpler queries, data cleanup | Lost data, no recovery |
| No pagination default | Simpler API | Potential performance issues |

---

## Future Enhancements

### Short Term
- [ ] JWT authentication
- [ ] Pagination on all list endpoints
- [ ] Unit and integration tests
- [ ] API rate limiting
- [ ] Search functionality

### Medium Term
- [ ] Soft delete for records
- [ ] Audit logging
- [ ] Export to CSV/Excel
- [ ] Email notifications
- [ ] Background tasks (Celery)

### Long Term
- [ ] Multi-currency support
- [ ] Multi-tenant architecture
- [ ] Real-time updates (WebSockets)
- [ ] Machine learning insights
- [ ] Mobile API optimizations

---

**Document Version:** 1.0  
**Last Updated:** January 2024
