# Mini Project 2: Simple REST API Server

A professional-grade REST API server with in-memory data store demonstrating CRUD operations, proper API design, validation, error handling, and logging.

## 📋 Features

✅ **CRUD Operations**: Complete Create, Read, Update, Delete functionality
✅ **Request Validation**: Comprehensive input validation for all endpoints
✅ **Proper HTTP Status Codes**: 200, 201, 400, 404, 500 appropriately used
✅ **Error Handling Middleware**: Centralized error handling with custom exceptions
✅ **Logging**: Request/response logging with structured output
✅ **Clean API Design**: RESTful endpoints with consistent response format
✅ **UUID Generation**: Unique IDs for each user resource

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python app.py
```

The API will start on `http://localhost:5000`

## 📚 API Endpoints

### Health Check
```http
GET /health
```
Returns server status.

### Get All Users
```http
GET /users
```
**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "John Doe",
      "email": "john@example.com",
      "age": 30,
      "created_at": "2026-03-03T12:00:00.000000",
      "updated_at": "2026-03-03T12:00:00.000000"
    }
  ],
  "count": 1,
  "timestamp": "2026-03-03T12:00:00.000000"
}
```

### Get User by ID
```http
GET /users/{id}
```
**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "created_at": "2026-03-03T12:00:00.000000",
    "updated_at": "2026-03-03T12:00:00.000000"
  },
  "timestamp": "2026-03-03T12:00:00.000000"
}
```
**Response (404):** User not found

### Create User
```http
POST /users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30
}
```
**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "created_at": "2026-03-03T12:00:00.000000",
    "updated_at": "2026-03-03T12:00:00.000000"
  },
  "message": "User created successfully",
  "timestamp": "2026-03-03T12:00:00.000000"
}
```
**Response (400):** Validation error

**Validation Rules:**
- `name` (required): Non-empty string
- `email` (required): Valid email format (contains @ and .)
- `age` (optional): Integer between 0-150

### Update User
```http
PUT /users/{id}
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "age": 28
}
```
**Response (200):** Updated user object
**Response (404):** User not found
**Response (400):** Validation error

**Notes:**
- All fields are optional
- Updated fields are validated the same as create
- `updated_at` timestamp is automatically updated

### Delete User
```http
DELETE /users/{id}
```
**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "created_at": "2026-03-03T12:00:00.000000",
    "updated_at": "2026-03-03T12:00:00.000000"
  },
  "message": "User deleted successfully",
  "timestamp": "2026-03-03T12:00:00.000000"
}
```
**Response (404):** User not found

## 📋 Testing Examples

### Using cURL

**Create user:**
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice Johnson","email":"alice@example.com","age":28}'
```

**Get all users:**
```bash
curl http://localhost:5000/users
```

**Get user by ID:**
```bash
curl http://localhost:5000/users/{id}
```

**Update user:**
```bash
curl -X PUT http://localhost:5000/users/{id} \
  -H "Content-Type: application/json" \
  -d '{"age":29}'
```

**Delete user:**
```bash
curl -X DELETE http://localhost:5000/users/{id}
```

**Health check:**
```bash
curl http://localhost:5000/health
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:5000"

# Create user
response = requests.post(f"{BASE_URL}/users", json={
    "name": "Bob Smith",
    "email": "bob@example.com",
    "age": 35
})
print(response.json())

# Get all users
response = requests.get(f"{BASE_URL}/users")
print(response.json())

# Get specific user
user_id = "your-user-id"
response = requests.get(f"{BASE_URL}/users/{user_id}")
print(response.json())

# Update user
response = requests.put(f"{BASE_URL}/users/{user_id}", json={
    "age": 36
})
print(response.json())

# Delete user
response = requests.delete(f"{BASE_URL}/users/{user_id}")
print(response.json())
```

## 🏗️ Architecture & Best Practices

### Validation
- All inputs are validated before processing
- Custom validation function for reusable logic
- Clear error messages for better UX

### Error Handling
- Custom `APIError` exception class
- Global error handlers for all HTTP status codes
- Consistent error response format

### Logging
- Request/response logging with timestamps
- Different log levels (INFO, WARNING, ERROR)
- Structured log messages for debugging

### Data Structure
- In-memory dictionary for O(1) lookups
- UUID for unique user identification
- Timestamps for audit trail

### HTTP Status Codes
- **200**: Successful GET, PUT, DELETE
- **201**: Successful POST (resource created)
- **400**: Bad request / validation error
- **404**: Resource not found
- **500**: Internal server error

## 🔒 Data Model

```python
{
    "id": "uuid",                    # Unique identifier
    "name": "string",                # User name (required)
    "email": "string",               # User email (required)
    "age": "integer or null",        # User age (optional)
    "created_at": "ISO timestamp",   # Creation time
    "updated_at": "ISO timestamp"    # Last update time
}
```

## 📝 Response Format

All responses follow a consistent structure:

**Success Response:**
```json
{
  "success": true,
  "data": {},
  "message": "Optional success message",
  "count": "Optional item count",
  "timestamp": "2026-03-03T12:00:00.000000"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message",
  "timestamp": "2026-03-03T12:00:00.000000"
}
```

## 🎯 What This Project Demonstrates

1. **REST API Design** - Proper endpoint structure and HTTP method usage
2. **CRUD Operations** - Complete resource lifecycle management
3. **Input Validation** - Comprehensive data validation patterns
4. **Error Handling** - Professional error handling and middleware
5. **Logging** - Application monitoring and debugging
6. **Code Organization** - Clean code structure with comments
7. **Type Hints** - Modern Python type annotations
8. **Documentation** - Clear docstrings and README

## 💡 Extension Ideas

- Add database persistence (SQLite, PostgreSQL)
- Add authentication and authorization
- Add rate limiting
- Add request/response compression
- Add API versioning
- Add Swagger/OpenAPI documentation
- Add unit tests
- Add Docker containerization

## 📄 License

Mini Project 2 - Learning Resource
