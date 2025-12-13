# Budget Categories Setup

## Overview

The backend now automatically creates default categories for each new user when they sign up. These categories can be used immediately when creating budgets and transactions.

## Default Categories Created

### Income Categories (5)
- **Salary** 💰 - Regular employment income
- **Freelance** 💻 - Freelance/contract work
- **Investment** 📈 - Investment returns
- **Bonus** 🎁 - Bonuses and one-time payments
- **Other Income** ✅ - Miscellaneous income

### Expense Categories (10)
- **Groceries** 🛒 - Food and groceries
- **Transport** 🚗 - Transportation costs
- **Utilities** 💡 - Bills and utilities
- **Entertainment** 🎮 - Entertainment and hobbies
- **Healthcare** 🏥 - Medical expenses
- **Dining** 🍽️ - Restaurants and eating out
- **Shopping** 🛍️ - Clothing and shopping
- **Education** 📚 - Education and learning
- **Insurance** 🛡️ - Insurance premiums
- **Other Expense** 📌 - Other expenses

## How It Works

### Automatic Creation (New Users)
When a user signs up:
1. User account is created
2. UserProfile is created
3. **Default categories are automatically created** ✅
4. User can immediately use these categories

### Management Command (Existing Users)
For users who signed up before this feature was added, run:

```bash
# Create categories for all users
python manage.py create_categories

# Create categories for specific user (by user ID)
python manage.py create_categories --user 1
```

## API Endpoints

### List All Categories
```
GET /api/budgets/categories/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "user": 1,
      "name": "Salary",
      "type": "income",
      "icon": "💰",
      "is_default": false,
      "created_at": "2025-12-13T17:00:00Z",
      "updated_at": "2025-12-13T17:00:00Z"
    },
    ...
  ]
}
```

### Filter by Type
```
GET /api/budgets/categories/?type=income
GET /api/budgets/categories/?type=expense
```

### Search Categories
```
GET /api/budgets/categories/?search=salary
```

### Create Custom Category
```
POST /api/budgets/categories/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Gifts",
  "type": "expense",
  "icon": "🎁",
  "description": "Gifts and donations"
}
```

**Response (201):**
```json
{
  "id": 16,
  "user": 1,
  "name": "Gifts",
  "type": "expense",
  "icon": "🎁",
  "description": "Gifts and donations",
  "is_default": false,
  "created_at": "2025-12-13T17:30:00Z",
  "updated_at": "2025-12-13T17:30:00Z"
}
```

### Update Category
```
PUT /api/budgets/categories/16/
Authorization: Bearer <access_token>

{
  "name": "Gifts & Donations",
  "icon": "❤️"
}
```

### Delete Category
```
DELETE /api/budgets/categories/16/
Authorization: Bearer <access_token>
```

## Frontend Integration

### Get All Categories
```javascript
import { useBudgetStore } from './store/budgetStore';

const { categories, fetchCategories } = useBudgetStore();

// Fetch categories
await fetchCategories();

// Get income categories
const incomeCategories = categories.filter(c => c.type === 'income');

// Get expense categories
const expenseCategories = categories.filter(c => c.type === 'expense');
```

### Create New Category
```javascript
const { createCategory } = useBudgetStore();

await createCategory({
  name: 'Pet Care',
  type: 'expense',
  icon: '🐾',
  description: 'Pet food and veterinary care'
});
```

### Get Category by Type
```javascript
const { getCategoriesByType } = useBudgetStore();

const expenses = getCategoriesByType('expense');
const incomes = getCategoriesByType('income');
```

## Troubleshooting

### Categories Not Showing

**Problem:** User signed up but doesn't see categories

**Solution:** Run the management command
```bash
python manage.py create_categories --user <user_id>
```

### Duplicate Categories Created

**Problem:** Multiple categories with same name for a user

**This shouldn't happen** - The model has `unique_together = ['user', 'name', 'type']` constraint.

If it occurs, it means they were created at the same time. Use the management command again:
```bash
python manage.py create_categories --user <user_id>
```

### Categories Not Loading in Frontend

**Problem:** API returns 401 Unauthorized

**Solution:**
1. Verify token is being sent in Authorization header: `Bearer <token>`
2. Check Django logs for errors
3. Ensure user is authenticated

## Database Schema

```python
class Category(models.Model):
    user = ForeignKey(User, null=True, blank=True)  # User-specific or default
    name = CharField(max_length=100)
    type = CharField(choices=['income', 'expense'])
    description = TextField(blank=True, null=True)
    icon = CharField(max_length=50, blank=True)
    is_default = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    unique_together = ['user', 'name', 'type']  # Prevent duplicates
```

## Key Features

✅ **Automatic Creation** - Categories created when user signs up
✅ **User-Specific** - Each user has their own categories
✅ **Unique Constraint** - No duplicate category names per user
✅ **Filtering** - Filter by type (income/expense)
✅ **Search** - Search categories by name
✅ **Icons** - Each category has an emoji icon
✅ **Manageable** - Can be created, updated, deleted via API
✅ **Portable** - Used by budgets, transactions, and goals

## Next Steps

1. ✅ Update `/api/auth/register/` to trigger category creation
2. ✅ Provide management command for existing users
3. Use categories in budget/transaction endpoints
4. Display categories in frontend category selector
5. Allow custom categories to be created by users

