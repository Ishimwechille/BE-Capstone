# Installation & Setup Guide

## Prerequisites

- **Python 3.8+** - Check with `python --version`
- **pip** - Python package manager (usually comes with Python)
- **git** - For version control (optional but recommended)
- **Virtual Environment** - Recommended for isolated Python environments

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ishimwechille/BE-Capstone.git
cd BE-Capstone
```

### 2. Create and Activate Virtual Environment

#### Windows (PowerShell)
```powershell
python -m venv venv
venv\Scripts\Activate
```

#### Windows (Command Prompt)
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

**Verify activation:** Your terminal should show `(venv)` at the beginning

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment (Optional)

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-very-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
- Username: `admin`
- Email: `admin@example.com`
- Password: (choose a strong password)

### 7. Load Default Categories (Optional)

Create a script or use the admin panel to load default categories:

```python
from budgets.models import Category

# Income categories
income_categories = [
    {'name': 'Salary', 'type': 'income'},
    {'name': 'Freelance', 'type': 'income'},
    {'name': 'Investment', 'type': 'income'},
    {'name': 'Bonus', 'type': 'income'},
    {'name': 'Other Income', 'type': 'income'},
]

# Expense categories
expense_categories = [
    {'name': 'Groceries', 'type': 'expense'},
    {'name': 'Dining Out', 'type': 'expense'},
    {'name': 'Transportation', 'type': 'expense'},
    {'name': 'Utilities', 'type': 'expense'},
    {'name': 'Entertainment', 'type': 'expense'},
    {'name': 'Shopping', 'type': 'expense'},
    {'name': 'Healthcare', 'type': 'expense'},
    {'name': 'Education', 'type': 'expense'},
    {'name': 'Subscriptions', 'type': 'expense'},
    {'name': 'Other Expense', 'type': 'expense'},
]

for cat in income_categories + expense_categories:
    Category.objects.get_or_create(**cat, defaults={'is_default': True})
```

### 8. Run Development Server

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000/`

## Accessing the Application

### API Endpoints
- **Base URL:** `http://localhost:8000/api/`
- **Documentation:** See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### Admin Panel
- **URL:** `http://localhost:8000/admin/`
- **Credentials:** Use the superuser account created in step 6

### Browsable API
Django REST Framework provides a browsable API:
- Navigate to any endpoint (e.g., `http://localhost:8000/api/auth/register/`)
- You'll see a web interface to test endpoints

## Testing the API

### Using Python requests library

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Register
response = requests.post(f"{BASE_URL}/auth/register/", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
})
print(response.json())

# Login
response = requests.post(f"{BASE_URL}/auth/login/", json={
    "username": "testuser",
    "password": "testpass123"
})
token = response.json()['token']

# Get profile (with token)
headers = {"Authorization": f"Token {token}"}
response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
print(response.json())
```

### Using Postman

1. Download and install [Postman](https://www.postman.com/downloads/)
2. Create a new collection for the Sentinel Tracker
3. Set up environment variables:
   - `BASE_URL`: `http://localhost:8000/api`
   - `TOKEN`: (leave empty, will be set after login)
4. Create requests for each endpoint
5. Use the pre-request script to automatically set the token:
   ```javascript
   if (pm.response.code === 200 && pm.response.json().token) {
       pm.environment.set("TOKEN", pm.response.json().token);
   }
   ```

### Using cURL

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# Get profile (replace TOKEN with actual token)
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Token TOKEN"
```

## Common Issues & Solutions

### Issue: "No module named 'django'"
**Solution:** Make sure virtual environment is activated and dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: "ModuleNotFoundError: No module named 'rest_framework'"
**Solution:** Install all dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Issue: "Port 8000 is already in use"
**Solution:** Run on a different port
```bash
python manage.py runserver 8001
```

### Issue: Database errors during migration
**Solution:** Reset the database (development only!)
```bash
# Remove the old database
rm db.sqlite3

# Re-run migrations
python manage.py migrate
python manage.py createsuperuser
```

### Issue: "CSRF token missing or incorrect"
**Solution:** This usually happens with POST requests. Ensure:
- You're sending the proper Content-Type header
- For API requests, use token authentication
- Check that CSRF middleware is properly configured

## Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test users
python manage.py test transactions
python manage.py test budgets
python manage.py test reports

# Run with verbose output
python manage.py test --verbosity=2

# Run specific test class
python manage.py test users.tests.UserTestCase

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates HTML coverage report
```

## Management Commands

### Check Budgets and Generate Alerts
```bash
# Check all users
python manage.py check_budgets

# Check specific user
python manage.py check_budgets --user_id=1

# With email notifications (if configured)
python manage.py check_budgets --send-email
```

### Create Default Categories
```bash
python manage.py shell
```

Then paste the code from step 7 above.

### Create Sample Data
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from budgets.models import Category, Budget, Goal
from transactions.models import Income, Expense
from datetime import date, datetime
from decimal import Decimal

# Get or create user
user = User.objects.first()

# Create categories if not exist
salary_cat, _ = Category.objects.get_or_create(
    name='Salary', type='income', defaults={'is_default': True}
)
groceries_cat, _ = Category.objects.get_or_create(
    name='Groceries', type='expense', defaults={'is_default': True}
)

# Add income
income = Income.objects.create(
    user=user,
    category=salary_cat,
    amount=Decimal('5000.00'),
    date=date.today(),
    description='Monthly salary'
)

# Add expense
expense = Expense.objects.create(
    user=user,
    category=groceries_cat,
    amount=Decimal('150.00'),
    date=date.today(),
    description='Weekly groceries'
)

# Create budget
budget = Budget.objects.create(
    user=user,
    category=groceries_cat,
    limit_amount=Decimal('500.00'),
    start_date=date(2025, 12, 1),
    end_date=date(2025, 12, 31)
)

# Create goal
goal = Goal.objects.create(
    user=user,
    name='Emergency Fund',
    target_amount=Decimal('5000.00'),
    current_amount=Decimal('1000.00'),
    target_date=date(2026, 12, 31)
)

print("Sample data created successfully!")
```

## Database Operations

### Backup Database
```bash
# SQLite backup
cp db.sqlite3 db.sqlite3.backup
```

### Reset Database (Development Only!)
```bash
python manage.py flush
```

### Export Data
```bash
python manage.py dumpdata > backup.json
```

### Import Data
```bash
python manage.py loaddata backup.json
```

## Logging

Log configuration is set in `sentinel_tracker/settings.py`. By default, logs are sent to console.

To view logs at different levels:
```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

## Production Deployment

For production deployment:

1. **Set environment variables:**
   ```env
   DEBUG=False
   SECRET_KEY=<generate-a-strong-secret-key>
   ALLOWED_HOSTS=yourdomain.com
   ```

2. **Use a production database:**
   ```env
   DATABASE_ENGINE=django.db.backends.postgresql
   DATABASE_NAME=sentinel_tracker
   DATABASE_USER=postgres
   DATABASE_PASSWORD=<password>
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   ```

3. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Use a production server (Gunicorn):**
   ```bash
   pip install gunicorn
   gunicorn sentinel_tracker.wsgi
   ```

5. **Use a reverse proxy (Nginx):**
   Configure Nginx to forward requests to Gunicorn

6. **Set up SSL/TLS:**
   Use Let's Encrypt for free SSL certificates

## Useful Django Commands

```bash
# Create migrations for changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create a new app
python manage.py startapp appname

# Open Django shell
python manage.py shell

# Check project setup
python manage.py check

# Display all registered apps
python manage.py showmigrations

# Create a custom management command
python manage.py startapp management.commands.cmdname

# Run a specific migration
python manage.py migrate appname

# Revert a migration
python manage.py migrate appname 0001
```

## Getting Help

- **Django Documentation:** https://docs.djangoproject.com/
- **Django REST Framework:** https://www.django-rest-framework.org/
- **Project README:** See [README.md](README.md)
- **API Documentation:** See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

**Happy coding! 🚀**
