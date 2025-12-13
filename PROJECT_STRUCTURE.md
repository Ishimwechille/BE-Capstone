# Project Structure Overview

## The Sentinel Tracker - Backend Project Layout

```
BE-Capstone/
│
├── sentinel_tracker/              # Main Django project
│   ├── __init__.py
│   ├── settings.py               # Project configuration
│   ├── urls.py                   # Main URL router
│   ├── asgi.py                   # ASGI configuration
│   └── wsgi.py                   # WSGI configuration
│
├── users/                         # User authentication app
│   ├── migrations/               # Database migrations
│   ├── __init__.py
│   ├── admin.py                  # Admin panel configuration
│   ├── apps.py                   # App configuration
│   ├── models.py                 # UserProfile model
│   ├── views.py                  # Auth views (register, login, logout, profile)
│   ├── serializers.py            # User serializers
│   ├── signals.py                # Auto-create profile & token on user creation
│   ├── tests.py                  # Unit tests
│   └── urls.py                   # App URL routing
│
├── transactions/                  # Income & Expense tracking app
│   ├── migrations/               # Database migrations
│   ├── __init__.py
│   ├── admin.py                  # Admin panel configuration
│   ├── apps.py                   # App configuration
│   ├── models.py                 # Income, Expense models
│   ├── views.py                  # Transaction ViewSets
│   ├── serializers.py            # Transaction serializers
│   ├── tests.py                  # Unit tests
│   └── urls.py                   # App URL routing
│
├── budgets/                       # Budget & Category management app
│   ├── migrations/               # Database migrations
│   ├── __init__.py
│   ├── admin.py                  # Admin panel configuration
│   ├── apps.py                   # App configuration
│   ├── models.py                 # Category, Budget, Goal models
│   ├── views.py                  # Category, Budget, Goal ViewSets
│   ├── serializers.py            # Budget serializers
│   ├── tests.py                  # Unit tests
│   └── urls.py                   # App URL routing
│
├── reports/                       # Reporting & Alerts app
│   ├── management/               # Django management commands
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── check_budgets.py  # Background alert generation task
│   ├── migrations/               # Database migrations
│   ├── __init__.py
│   ├── admin.py                  # Admin panel configuration
│   ├── apps.py                   # App configuration
│   ├── models.py                 # Alert model
│   ├── views.py                  # Report ViewSet, Alert ViewSet
│   ├── serializers.py            # Alert serializer
│   ├── logic.py                  # Report calculation functions
│   ├── tests.py                  # Unit tests
│   └── urls.py                   # App URL routing
│
├── manage.py                      # Django management script
├── requirements.txt              # Python dependencies
│
├── README.md                     # Project overview & getting started
├── INSTALLATION.md               # Detailed installation guide
├── API_DOCUMENTATION.md          # Complete API endpoint documentation
├── PROJECT_STRUCTURE.md          # This file
│
├── .gitignore                    # Git ignore rules
├── db.sqlite3                    # SQLite database (development only)
└── .git/                         # Git repository
```

## File Descriptions

### Core Django Files

| File | Purpose |
|------|---------|
| `manage.py` | Django CLI for running commands and starting server |
| `sentinel_tracker/settings.py` | All project configuration (apps, middleware, database, etc.) |
| `sentinel_tracker/urls.py` | Main URL router that includes all app URLs |
| `sentinel_tracker/asgi.py` | ASGI application for deployment with async support |
| `sentinel_tracker/wsgi.py` | WSGI application for traditional deployment |

### App Structure (repeated for each app)

| File | Purpose |
|------|---------|
| `models.py` | Database models and relationships |
| `views.py` | API views/viewsets handling requests |
| `serializers.py` | Data serialization/validation |
| `urls.py` | App-specific URL routing |
| `admin.py` | Django admin panel configuration |
| `apps.py` | App configuration and metadata |
| `tests.py` | Unit and integration tests |
| `migrations/` | Database schema changes |

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview, features, and quick start |
| `INSTALLATION.md` | Detailed setup and installation instructions |
| `API_DOCUMENTATION.md` | Complete API endpoint reference |
| `PROJECT_STRUCTURE.md` | This file - project organization |

## App Responsibilities

### `users` App
- User authentication (register, login, logout)
- User profiles and preferences
- Token generation and management
- User data validation

### `transactions` App
- Create, read, update, delete income records
- Create, read, update, delete expense records
- Transaction filtering and search
- Monthly transaction summaries

### `budgets` App
- Category CRUD operations
- Budget CRUD operations (spending limits)
- Financial goals tracking
- Budget vs. actual spending calculations
- Goal progress monitoring

### `reports` App
- Generate monthly financial summaries
- Calculate expense breakdown by category
- Track budget consumption status
- Project end-of-month spending
- Manage alerts and notifications
- Background task for alert generation

## Data Models Overview

### User-Related
```
User (Django built-in)
└─ UserProfile (extended user info)
```

### Transactions
```
Income
├─ user
├─ category
└─ amount

Expense
├─ user
├─ category
└─ amount
```

### Budgets & Goals
```
Category
├─ name
├─ type (income/expense)
└─ user

Budget
├─ user
├─ category
├─ limit_amount
└─ period (start_date to end_date)

Goal
├─ user
├─ name
├─ target_amount
└─ target_date
```

### Reports
```
Alert
├─ user
├─ type (danger/success/tip/info)
└─ related_category
```

## URL Structure

```
/api/
├── auth/
│   ├── register/
│   ├── login/
│   ├── logout/
│   └── profile/
│
├── transactions/
│   ├── income/              (ViewSet)
│   │   └── {id}/by_month/
│   └── expenses/            (ViewSet)
│       ├── {id}/by_month/
│       └── {id}/by_category/
│
├── budgets/
│   ├── categories/          (ViewSet)
│   ├── budgets/             (ViewSet)
│   │   ├── current_month/
│   │   └── exceeded/
│   └── goals/               (ViewSet)
│       ├── active/
│       └── {id}/update_progress/
│
└── reports/
    ├── summary/             (ViewSet action)
    ├── breakdown/           (ViewSet action)
    ├── budget_status/       (ViewSet action)
    ├── spending_projection/ (ViewSet action)
    ├── dashboard/           (ViewSet action)
    └── alerts/              (ViewSet)
        ├── {id}/mark_as_read/
        ├── mark_all_as_read/
        └── unread/
```

## Database Relationships

### Foreign Key Relationships
- `UserProfile` → `User` (One-to-One)
- `Income` → `User` (Many-to-One)
- `Income` → `Category` (Many-to-One)
- `Expense` → `User` (Many-to-One)
- `Expense` → `Category` (Many-to-One)
- `Budget` → `User` (Many-to-One)
- `Budget` → `Category` (Many-to-One)
- `Goal` → `User` (Many-to-One)
- `Goal` → `Category` (Many-to-One, optional)
- `Alert` → `User` (Many-to-One)

## Workflow Flow

```
User
│
├─ Registers → creates User + Token + UserProfile
│
├─ Logs in → receives Token
│
├─ Creates Categories (can use defaults)
│
├─ Records Transactions
│   ├─ Income records
│   └─ Expense records
│
├─ Sets Budgets
│   └─ Links categories to spending limits
│
├─ Defines Financial Goals
│   └─ Long-term savings targets
│
└─ Views Reports
    ├─ Monthly summary
    ├─ Category breakdown
    ├─ Budget status
    ├─ Spending projections
    └─ Alerts
        └─ Generated by check_budgets command
```

## Key Features by App

### Users
- ✅ Registration with validation
- ✅ Token-based authentication
- ✅ User profile management
- ✅ Base currency preferences

### Transactions
- ✅ CRUD for income/expenses
- ✅ Multi-currency support
- ✅ Transaction filtering
- ✅ Monthly summaries

### Budgets
- ✅ Category management
- ✅ Budget creation and tracking
- ✅ Budget utilization calculations
- ✅ Goal management
- ✅ Progress tracking

### Reports
- ✅ Monthly financial summaries
- ✅ Category breakdowns
- ✅ Budget status monitoring
- ✅ Spending projections
- ✅ Alert system
- ✅ Background task scheduling

## Development Tips

1. **Always use ViewSets** for CRUD operations (they're more efficient)
2. **Use serializers** for data validation and transformation
3. **Filter querysets** to current user for security
4. **Add proper pagination** for large datasets
5. **Document all endpoints** in API_DOCUMENTATION.md
6. **Write tests** for all business logic
7. **Use management commands** for background tasks

## Deployment Considerations

- Change `DEBUG=False` in production
- Use environment variables for sensitive data
- Set up proper logging
- Configure email for alerts
- Use PostgreSQL instead of SQLite
- Enable HTTPS/SSL
- Set up CORS properly
- Use a production WSGI server (Gunicorn)
- Implement proper error handling and monitoring

---

For detailed setup instructions, see [INSTALLATION.md](INSTALLATION.md)

For API endpoint documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

For general project information, see [README.md](README.md)
