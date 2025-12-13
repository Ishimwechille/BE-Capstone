# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Run Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000/` 🎉

---

## 📚 Quick API Test

### Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

Save the `token` from the response, then use it:

```bash
TOKEN="your-token-here"
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Token $TOKEN"
```

---

## 🎯 Next Steps

1. **Read the full documentation:** Check out [README.md](README.md)
2. **Explore the API:** See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
3. **Setup complete guide:** Follow [INSTALLATION.md](INSTALLATION.md)
4. **Learn the structure:** Review [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

## 🔑 Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/register/` | Create new user |
| POST | `/api/auth/login/` | Get auth token |
| GET | `/api/transactions/income/` | List income |
| POST | `/api/transactions/income/` | Add income |
| GET | `/api/transactions/expenses/` | List expenses |
| POST | `/api/transactions/expenses/` | Add expense |
| GET | `/api/reports/summary/` | Monthly summary |
| GET | `/api/reports/dashboard/` | Full dashboard |

---

## ⚙️ Common Commands

```bash
# Create migrations for model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Run admin panel
python manage.py runserver
# Then visit http://localhost:8000/admin/

# Run tests
python manage.py test

# Generate alerts
python manage.py check_budgets

# Reset database (development only!)
python manage.py flush
```

---

## 🆘 Troubleshooting

**Problem:** Port 8000 already in use
```bash
python manage.py runserver 8001
```

**Problem:** Database errors
```bash
rm db.sqlite3
python manage.py migrate
```

**Problem:** Module not found
```bash
pip install -r requirements.txt
```

---

## 📖 Documentation

- 📘 [Full README](README.md)
- 📗 [API Documentation](API_DOCUMENTATION.md)
- 📙 [Installation Guide](INSTALLATION.md)
- 📓 [Project Structure](PROJECT_STRUCTURE.md)

---

**Happy building! 🎊**

For detailed information, check the other documentation files or visit the GitHub repository.
