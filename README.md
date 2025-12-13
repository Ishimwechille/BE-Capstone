# The Sentinel Tracker - Advanced Expense & Goal Manager

A proactive personal financial management system built with Django REST Framework. This backend API enables users to track income and expenses, set granular budgets, define financial goals, and receive automated alerts based on spending patterns.

## 🎯 Project Overview

**The Sentinel Tracker** is a comprehensive financial management solution that goes beyond simple transaction logging. It provides intelligent budget monitoring, goal tracking, and an automated alert system that helps users stay on top of their finances.

### Key Features

#### MVP (Core Functionality - Weeks 1-3)
- ✅ **User Authentication & Authorization** - Secure token-based API access
- ✅ **Transaction Management** - Full CRUD for Income and Expense records
- ✅ **Category Management** - User-defined and default categories
- ✅ **Budget Management** - Set spending limits by category over specific periods
- ✅ **Basic Reporting** - Monthly summaries, category breakdowns, and net balance calculations

#### Advanced Features (Weeks 4-5)
- 🔄 **Proactive Alert System** - Automated daily checks for budget warnings and success alerts
- 🎯 **Financial Goals** - Define long-term savings targets with progress tracking
- 💱 **Multi-Currency Support** - Convert expenses in foreign currencies to base currency
- 📊 **Spending Projections** - AI-powered predictions for end-of-month spending

## 📋 Project Structure

```
sentinel_tracker/
├── users/                      # User authentication and profiles
│   ├── models.py              # UserProfile model
│   ├── views.py               # Register, Login, Logout, Profile endpoints
│   ├── serializers.py         # User serialization
│   ├── signals.py             # Auto-create profile and token on user creation
│   └── urls.py
│
├── transactions/              # Income and expense tracking
│   ├── models.py              # Income, Expense models
│   ├── views.py               # Transaction CRUD ViewSets
│   ├── serializers.py         # Transaction serialization
│   └── urls.py
│
├── budgets/                   # Category and budget management
│   ├── models.py              # Category, Budget, Goal models
│   ├── views.py               # Category, Budget, Goal ViewSets
│   ├── serializers.py         # Budget serialization
│   └── urls.py
│
├── reports/                   # Financial reporting and alerts
│   ├── models.py              # Alert model
│   ├── logic.py               # Report calculation functions
│   ├── views.py               # Report and Alert endpoints
│   ├── serializers.py         # Alert serialization
│   ├── management/
│   │   └── commands/
│   │       └── check_budgets.py  # Background task for alerts
│   └── urls.py
│
├── sentinel_tracker/
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL router
│   ├── asgi.py                # ASGI config
│   └── wsgi.py                # WSGI config
│
├── manage.py                  # Django management script
├── requirements.txt           # Project dependencies
└── db.sqlite3                # SQLite database (development)
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register/` - Create a new user account
- `POST /api/auth/login/` - Get authentication token
- `POST /api/auth/logout/` - Logout (invalidate token)
- `GET /api/auth/profile/` - Get current user profile

### Transactions
- `GET/POST /api/transactions/income/` - List/Create income records
- `GET/POST /api/transactions/expenses/` - List/Create expense records
- `GET /api/transactions/income/{id}/by_month/` - Monthly income summary
- `GET /api/transactions/expenses/{id}/by_month/` - Monthly expense summary
- `GET /api/transactions/expenses/{id}/by_category/` - Expense breakdown by category

### Budgets & Categories
- `GET/POST /api/budgets/categories/` - Manage categories
- `GET/POST /api/budgets/budgets/` - Manage budgets
- `GET /api/budgets/budgets/current_month/` - Current month budgets
- `GET /api/budgets/budgets/exceeded/` - Exceeded budgets
- `GET/POST /api/budgets/goals/` - Manage financial goals
- `GET /api/budgets/goals/active/` - Active goals only
- `POST /api/budgets/goals/{id}/update_progress/` - Update goal progress

### Reports & Alerts
- `GET /api/reports/summary/` - Monthly financial summary
- `GET /api/reports/breakdown/` - Category spending breakdown
- `GET /api/reports/budget_status/` - Current budget status
- `GET /api/reports/spending_projection/` - Month-end spending projection
- `GET /api/reports/dashboard/` - Comprehensive dashboard data
- `GET /api/reports/alerts/` - List all alerts
- `POST /api/reports/alerts/{id}/mark_as_read/` - Mark alert as read
- `POST /api/reports/alerts/mark_all_as_read/` - Mark all alerts as read

## 🗄️ Database Models

### User (Django Built-in)
Extended with `UserProfile` for additional data like base currency and profile info.

### Category
```
- name: CharField
- type: CharField (income/expense)
- user: ForeignKey (User, optional for default categories)
- description: TextField
- icon: CharField
- is_default: BooleanField
```

### Income
```
- user: ForeignKey (User)
- category: ForeignKey (Category)
- amount: DecimalField
- date: DateField
- description: TextField
```

### Expense
```
- user: ForeignKey (User)
- category: ForeignKey (Category)
- amount: DecimalField (in base currency)
- original_amount: DecimalField (in original currency)
- currency: CharField (ISO currency code)
- exchange_rate: DecimalField
- date: DateField
- description: TextField
```

### Budget
```
- user: ForeignKey (User)
- category: ForeignKey (Category)
- limit_amount: DecimalField
- start_date: DateField
- end_date: DateField
```

### Goal
```
- user: ForeignKey (User)
- name: CharField
- target_amount: DecimalField
- current_amount: DecimalField
- target_date: DateField
- is_completed: BooleanField
```

### Alert
```
- user: ForeignKey (User)
- title: CharField
- message: TextField
- alert_type: CharField (danger/success/tip/info)
- is_read: BooleanField
- related_category: CharField
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip/pipenv
- Virtual environment

### Installation

1. **Clone the repository**
```bash
git clone <repo-url>
cd BE-Capstone
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables** (Optional)
Create a `.env` file in the root directory:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser** (for admin panel)
```bash
python manage.py createsuperuser
```

7. **Run the development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## 📖 Usage Examples

### Register a New User
```bash
POST /api/auth/register/
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password2": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
}
```

### Login and Get Token
```bash
POST /api/auth/login/
{
    "username": "john_doe",
    "password": "securepass123"
}

Response:
{
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com"
    },
    "token": "abc123def456..."
}
```

### Add Token to Headers
All subsequent requests must include:
```
Authorization: Token abc123def456...
```

### Create an Expense
```bash
POST /api/transactions/expenses/
{
    "category": 1,
    "amount": "50.00",
    "date": "2025-12-13",
    "description": "Grocery shopping",
    "currency": "USD"
}
```

### Set a Budget
```bash
POST /api/budgets/budgets/
{
    "category": 1,
    "limit_amount": "500.00",
    "start_date": "2025-12-01",
    "end_date": "2025-12-31"
}
```

### Get Monthly Summary
```bash
GET /api/reports/summary/?year=2025&month=12

Response:
{
    "year": 2025,
    "month": 12,
    "total_income": 5000.00,
    "total_expense": 2300.00,
    "net_balance": 2700.00,
    "income_count": 5,
    "expense_count": 23
}
```

## 🔐 Security Features

- **Token-based Authentication**: Uses Django REST Framework's token authentication
- **Permission Classes**: All endpoints (except register/login) require authentication
- **CORS Protection**: Configured to accept requests from trusted origins only
- **User Isolation**: Users can only access their own data
- **Password Validation**: Enforces strong password requirements

## 📊 Dashboard Endpoint

The comprehensive dashboard endpoint combines all reporting data:

```bash
GET /api/reports/dashboard/?year=2025&month=12
```

Returns:
- Monthly summary (income, expenses, balance)
- Category breakdown
- Budget status for all active budgets
- Spending projection for the rest of the month

## 🔄 Background Tasks

The alert system will be triggered by a Django Management Command:

```bash
python manage.py check_budgets
```

This command:
1. Checks all active budgets against current spending
2. Generates "danger" alerts if spending exceeds budget
3. Generates "success" alerts for well-managed budgets
4. Updates goal progress automatically

To run this automatically, schedule it with a Cron job (Linux/macOS) or Task Scheduler (Windows).

## 📝 Testing

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test users
python manage.py test transactions
python manage.py test budgets
python manage.py test reports

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🛠️ Development Tools

- **Django Admin Panel**: `http://localhost:8000/admin/`
- **API Documentation**: Available via DRF's browsable API
- **Postman Collection**: (To be created for manual testing)

## 📅 Project Timeline

| Week | Focus | Status |
|------|-------|--------|
| 1 | Foundation & Transactions | Planning |
| 2 | Budgeting & Categories | Planning |
| 3 | Reporting & Data Logic | Planning |
| 4 | Advanced Alerts & Goals | Planning |
| 5 | Testing, Documentation, & QA | Planning |

## 🤝 Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit your changes (`git commit -m 'Add amazing feature'`)
3. Push to the branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## 📄 License

This project is part of the ALX Capstone Program.

## 📞 Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Built with ❤️ for the ALX Capstone Project**
