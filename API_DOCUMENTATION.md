# API Documentation - The Sentinel Tracker

## Base URL
```
http://localhost:8000/api/
```

## Authentication
All endpoints (except `/auth/register/` and `/auth/login/`) require token authentication.

**Header:**
```
Authorization: Token <your_token_here>
```

---

## Authentication Endpoints

### 1. Register User
**Endpoint:** `POST /auth/register/`

**Request:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password2": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "profile": {
            "id": 1,
            "bio": null,
            "phone_number": null,
            "base_currency": "USD",
            "created_at": "2025-12-13T10:00:00Z",
            "updated_at": "2025-12-13T10:00:00Z"
        }
    },
    "token": "abc123def456..."
}
```

---

### 2. Login User
**Endpoint:** `POST /auth/login/`

**Request:**
```json
{
    "username": "john_doe",
    "password": "securepass123"
}
```

**Response (200 OK):**
```json
{
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "profile": {
            "id": 1,
            "bio": null,
            "phone_number": null,
            "base_currency": "USD",
            "created_at": "2025-12-13T10:00:00Z",
            "updated_at": "2025-12-13T10:00:00Z"
        }
    },
    "token": "abc123def456..."
}
```

---

### 3. Get User Profile
**Endpoint:** `GET /auth/profile/`

**Response (200 OK):**
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "profile": {
        "id": 1,
        "bio": "Finance enthusiast",
        "phone_number": "+1234567890",
        "base_currency": "USD",
        "created_at": "2025-12-13T10:00:00Z",
        "updated_at": "2025-12-13T10:00:00Z"
    }
}
```

---

### 4. Logout
**Endpoint:** `POST /auth/logout/`

**Response (200 OK):**
```json
{
    "message": "Successfully logged out"
}
```

---

## Transaction Endpoints

### 5. List Income Records
**Endpoint:** `GET /transactions/income/`

**Query Parameters:**
- `category`: Filter by category ID
- `date`: Filter by specific date
- `search`: Search in description
- `ordering`: Order by field (date, amount, created_at)
- `page`: Pagination page number

**Response (200 OK):**
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": 1,
            "category": 1,
            "category_name": "Salary",
            "amount": "5000.00",
            "date": "2025-12-01",
            "description": "Monthly salary",
            "created_at": "2025-12-01T10:00:00Z",
            "updated_at": "2025-12-01T10:00:00Z"
        }
    ]
}
```

---

### 6. Create Income Record
**Endpoint:** `POST /transactions/income/`

**Request:**
```json
{
    "category": 1,
    "amount": "5000.00",
    "date": "2025-12-01",
    "description": "Monthly salary"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "user": 1,
    "category": 1,
    "category_name": "Salary",
    "amount": "5000.00",
    "date": "2025-12-01",
    "description": "Monthly salary",
    "created_at": "2025-12-01T10:00:00Z",
    "updated_at": "2025-12-01T10:00:00Z"
}
```

---

### 7. List Expenses
**Endpoint:** `GET /transactions/expenses/`

**Query Parameters:**
- `category`: Filter by category ID
- `date`: Filter by specific date
- `currency`: Filter by currency
- `search`: Search in description
- `ordering`: Order by field (date, amount, created_at)
- `page`: Pagination page number

**Response (200 OK):**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/transactions/expenses/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": 1,
            "category": 2,
            "category_name": "Groceries",
            "amount": "75.50",
            "date": "2025-12-12",
            "description": "Weekly groceries",
            "currency": "USD",
            "original_amount": "75.50",
            "exchange_rate": "1.0000",
            "created_at": "2025-12-12T15:30:00Z",
            "updated_at": "2025-12-12T15:30:00Z"
        }
    ]
}
```

---

### 8. Create Expense
**Endpoint:** `POST /transactions/expenses/`

**Request:**
```json
{
    "category": 2,
    "amount": "75.50",
    "date": "2025-12-12",
    "description": "Weekly groceries",
    "currency": "USD",
    "original_amount": "75.50",
    "exchange_rate": "1.0000"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "user": 1,
    "category": 2,
    "category_name": "Groceries",
    "amount": "75.50",
    "date": "2025-12-12",
    "description": "Weekly groceries",
    "currency": "USD",
    "original_amount": "75.50",
    "exchange_rate": "1.0000",
    "created_at": "2025-12-12T15:30:00Z",
    "updated_at": "2025-12-12T15:30:00Z"
}
```

---

## Budget Endpoints

### 9. List Categories
**Endpoint:** `GET /budgets/categories/`

**Query Parameters:**
- `type`: Filter by type (income/expense)
- `is_default`: Filter by default status
- `search`: Search by name

**Response (200 OK):**
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": null,
            "name": "Salary",
            "type": "income",
            "description": "Income from employment",
            "icon": "💰",
            "is_default": true,
            "created_at": "2025-12-13T10:00:00Z",
            "updated_at": "2025-12-13T10:00:00Z"
        }
    ]
}
```

---

### 10. Create Category
**Endpoint:** `POST /budgets/categories/`

**Request:**
```json
{
    "name": "Entertainment",
    "type": "expense",
    "description": "Movies, games, etc.",
    "icon": "🎬"
}
```

**Response (201 Created):**
```json
{
    "id": 11,
    "user": 1,
    "name": "Entertainment",
    "type": "expense",
    "description": "Movies, games, etc.",
    "icon": "🎬",
    "is_default": false,
    "created_at": "2025-12-13T10:15:00Z",
    "updated_at": "2025-12-13T10:15:00Z"
}
```

---

### 11. List Budgets
**Endpoint:** `GET /budgets/budgets/`

**Query Parameters:**
- `category`: Filter by category ID
- `start_date`: Filter by start date
- `end_date`: Filter by end date
- `ordering`: Order by field

**Response (200 OK):**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": 1,
            "category": 2,
            "category_name": "Groceries",
            "limit_amount": "500.00",
            "spent_amount": "200.00",
            "remaining_amount": "300.00",
            "start_date": "2025-12-01",
            "end_date": "2025-12-31",
            "created_at": "2025-12-01T10:00:00Z",
            "updated_at": "2025-12-01T10:00:00Z"
        }
    ]
}
```

---

### 12. Create Budget
**Endpoint:** `POST /budgets/budgets/`

**Request:**
```json
{
    "category": 2,
    "limit_amount": "500.00",
    "start_date": "2025-12-01",
    "end_date": "2025-12-31"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "user": 1,
    "category": 2,
    "category_name": "Groceries",
    "limit_amount": "500.00",
    "spent_amount": "0.00",
    "remaining_amount": "500.00",
    "start_date": "2025-12-01",
    "end_date": "2025-12-31",
    "created_at": "2025-12-01T10:00:00Z",
    "updated_at": "2025-12-01T10:00:00Z"
}
```

---

### 13. Get Budgets for Current Month
**Endpoint:** `GET /budgets/budgets/current_month/`

**Query Parameters:**
- `year`: Year (optional, defaults to current)
- `month`: Month (optional, defaults to current)

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "user": 1,
        "category": 2,
        "category_name": "Groceries",
        "limit_amount": "500.00",
        "spent_amount": "200.00",
        "remaining_amount": "300.00",
        "start_date": "2025-12-01",
        "end_date": "2025-12-31",
        "created_at": "2025-12-01T10:00:00Z",
        "updated_at": "2025-12-01T10:00:00Z"
    }
]
```

---

### 14. Get Exceeded Budgets
**Endpoint:** `GET /budgets/budgets/exceeded/`

**Response (200 OK):**
```json
[
    {
        "id": 2,
        "user": 1,
        "category": 3,
        "category_name": "Dining Out",
        "limit_amount": "200.00",
        "spent_amount": "250.00",
        "remaining_amount": "-50.00",
        "start_date": "2025-12-01",
        "end_date": "2025-12-31",
        "created_at": "2025-12-01T10:00:00Z",
        "updated_at": "2025-12-15T15:00:00Z"
    }
]
```

---

### 15. List Goals
**Endpoint:** `GET /budgets/goals/`

**Query Parameters:**
- `category`: Filter by category ID
- `is_completed`: Filter by completion status
- `ordering`: Order by field

**Response (200 OK):**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": 1,
            "name": "New Laptop",
            "description": "Save for a new laptop",
            "target_amount": "1500.00",
            "current_amount": "500.00",
            "target_date": "2026-06-01",
            "category": 1,
            "category_name": "Savings",
            "is_completed": false,
            "progress_percentage": 33.33,
            "remaining_amount": "1000.00",
            "days_remaining": 171,
            "created_at": "2025-12-01T10:00:00Z",
            "updated_at": "2025-12-13T10:00:00Z"
        }
    ]
}
```

---

### 16. Create Goal
**Endpoint:** `POST /budgets/goals/`

**Request:**
```json
{
    "name": "Vacation Fund",
    "description": "Summer vacation to Europe",
    "target_amount": "3000.00",
    "target_date": "2026-07-01",
    "category": 1
}
```

**Response (201 Created):**
```json
{
    "id": 2,
    "user": 1,
    "name": "Vacation Fund",
    "description": "Summer vacation to Europe",
    "target_amount": "3000.00",
    "current_amount": "0.00",
    "target_date": "2026-07-01",
    "category": 1,
    "category_name": "Savings",
    "is_completed": false,
    "progress_percentage": 0.0,
    "remaining_amount": "3000.00",
    "days_remaining": 200,
    "created_at": "2025-12-13T10:30:00Z",
    "updated_at": "2025-12-13T10:30:00Z"
}
```

---

### 17. Get Active Goals
**Endpoint:** `GET /budgets/goals/active/`

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "user": 1,
        "name": "New Laptop",
        "description": "Save for a new laptop",
        "target_amount": "1500.00",
        "current_amount": "500.00",
        "target_date": "2026-06-01",
        "category": 1,
        "category_name": "Savings",
        "is_completed": false,
        "progress_percentage": 33.33,
        "remaining_amount": "1000.00",
        "days_remaining": 171,
        "created_at": "2025-12-01T10:00:00Z",
        "updated_at": "2025-12-13T10:00:00Z"
    }
]
```

---

### 18. Update Goal Progress
**Endpoint:** `POST /budgets/goals/{id}/update_progress/`

**Request:**
```json
{
    "current_amount": "750.00"
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "user": 1,
    "name": "New Laptop",
    "description": "Save for a new laptop",
    "target_amount": "1500.00",
    "current_amount": "750.00",
    "target_date": "2026-06-01",
    "category": 1,
    "category_name": "Savings",
    "is_completed": false,
    "progress_percentage": 50.0,
    "remaining_amount": "750.00",
    "days_remaining": 171,
    "created_at": "2025-12-01T10:00:00Z",
    "updated_at": "2025-12-13T10:45:00Z"
}
```

---

## Report Endpoints

### 19. Monthly Summary
**Endpoint:** `GET /reports/summary/`

**Query Parameters:**
- `year`: Year (optional, defaults to current)
- `month`: Month (optional, defaults to current)

**Response (200 OK):**
```json
{
    "year": 2025,
    "month": 12,
    "total_income": "5000.00",
    "total_expense": "2300.00",
    "net_balance": "2700.00",
    "income_count": 5,
    "expense_count": 23
}
```

---

### 20. Category Breakdown
**Endpoint:** `GET /reports/breakdown/`

**Query Parameters:**
- `year`: Year (optional, defaults to current)
- `month`: Month (optional, defaults to current)

**Response (200 OK):**
```json
{
    "year": 2025,
    "month": 12,
    "breakdown": [
        {
            "category__name": "Groceries",
            "category__id": 2,
            "total": "450.00",
            "count": 12
        },
        {
            "category__name": "Dining Out",
            "category__id": 3,
            "total": "250.00",
            "count": 8
        },
        {
            "category__name": "Utilities",
            "category__id": 4,
            "total": "150.00",
            "count": 3
        }
    ],
    "total_expenses": "2300.00"
}
```

---

### 21. Budget Status
**Endpoint:** `GET /reports/budget_status/`

**Response (200 OK):**
```json
{
    "current_date": "2025-12-13",
    "budgets": [
        {
            "id": 1,
            "category": "Groceries",
            "limit_amount": 500.0,
            "spent": 200.0,
            "remaining": 300.0,
            "percentage": 40.0,
            "exceeded": false
        },
        {
            "id": 2,
            "category": "Dining Out",
            "limit_amount": 200.0,
            "spent": 250.0,
            "remaining": -50.0,
            "percentage": 125.0,
            "exceeded": true
        }
    ],
    "total_active_budgets": 2,
    "exceeded_count": 1
}
```

---

### 22. Spending Projection
**Endpoint:** `GET /reports/spending_projection/`

**Query Parameters:**
- `category`: Category ID (optional, for specific category projection)

**Response (200 OK):**
```json
{
    "current_date": "2025-12-13",
    "days_passed": 13,
    "days_remaining": 18,
    "current_spent": "900.00",
    "daily_average": 69.23,
    "projected_end_of_month": "2146.14",
    "category": "All"
}
```

---

### 23. Dashboard (Comprehensive)
**Endpoint:** `GET /reports/dashboard/`

**Query Parameters:**
- `year`: Year (optional, defaults to current)
- `month`: Month (optional, defaults to current)

**Response (200 OK):**
```json
{
    "summary": {
        "year": 2025,
        "month": 12,
        "total_income": "5000.00",
        "total_expense": "2300.00",
        "net_balance": "2700.00",
        "income_count": 5,
        "expense_count": 23
    },
    "breakdown": {
        "year": 2025,
        "month": 12,
        "breakdown": [...],
        "total_expenses": "2300.00"
    },
    "budget_status": {
        "current_date": "2025-12-13",
        "budgets": [...],
        "total_active_budgets": 2,
        "exceeded_count": 1
    },
    "spending_projection": {
        "current_date": "2025-12-13",
        "days_passed": 13,
        "days_remaining": 18,
        "current_spent": "900.00",
        "daily_average": 69.23,
        "projected_end_of_month": "2146.14",
        "category": "All"
    }
}
```

---

### 24. List Alerts
**Endpoint:** `GET /reports/alerts/`

**Query Parameters:**
- `alert_type`: Filter by type (danger/success/tip/info)
- `is_read`: Filter by read status
- `ordering`: Order by created_at
- `page`: Pagination page number

**Response (200 OK):**
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": 1,
            "title": "⚠️ Budget Exceeded: Dining Out",
            "message": "You have exceeded your budget for Dining Out!...",
            "alert_type": "danger",
            "is_read": false,
            "related_category": "Dining Out",
            "created_at": "2025-12-13T10:00:00Z",
            "updated_at": "2025-12-13T10:00:00Z"
        }
    ]
}
```

---

### 25. Mark Alert as Read
**Endpoint:** `POST /reports/alerts/{id}/mark_as_read/`

**Response (200 OK):**
```json
{
    "id": 1,
    "user": 1,
    "title": "⚠️ Budget Exceeded: Dining Out",
    "message": "You have exceeded your budget for Dining Out!...",
    "alert_type": "danger",
    "is_read": true,
    "related_category": "Dining Out",
    "created_at": "2025-12-13T10:00:00Z",
    "updated_at": "2025-12-13T10:05:00Z"
}
```

---

### 26. Mark All Alerts as Read
**Endpoint:** `POST /reports/alerts/mark_all_as_read/`

**Response (200 OK):**
```json
{
    "message": "5 alerts marked as read"
}
```

---

### 27. Get Unread Alerts
**Endpoint:** `GET /reports/alerts/unread/`

**Response (200 OK):**
```json
{
    "count": 2,
    "alerts": [
        {
            "id": 1,
            "user": 1,
            "title": "⚠️ Budget Exceeded: Dining Out",
            "message": "You have exceeded your budget for Dining Out!...",
            "alert_type": "danger",
            "is_read": false,
            "related_category": "Dining Out",
            "created_at": "2025-12-13T10:00:00Z",
            "updated_at": "2025-12-13T10:00:00Z"
        }
    ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
    "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error"
}
```

---

## Rate Limiting & Pagination

- **Page Size:** 20 items per page (configurable in settings)
- **Pagination Format:** Uses page number pagination

Example paginated response:
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/endpoint/?page=2",
    "previous": null,
    "results": [...]
}
```

---

## Query Parameter Examples

### Filter by Date Range
```
GET /api/transactions/expenses/?date=2025-12-13
```

### Search
```
GET /api/transactions/expenses/?search=grocery
```

### Multiple Filters
```
GET /api/budgets/budgets/?category=2&ordering=-limit_amount
```

---

## Helpful Tips

1. **Always include the Authorization header** for authenticated endpoints
2. **Use query parameters** for filtering and pagination
3. **Check the `count` field** to see total results
4. **Use `next` and `previous`** URLs for pagination
5. **Amounts are always returned as strings** to preserve precision
6. **Dates should be in ISO format** (YYYY-MM-DD)

---

For more information, visit the [README.md](README.md) or check the [GitHub repository](https://github.com/Ishimwechille/BE-Capstone).
