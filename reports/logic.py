"""Reports app business logic for summary and breakdown calculations."""
from django.db.models import Sum
from datetime import datetime, date, timedelta
from transactions.models import Income, Expense
from budgets.models import Budget


def get_monthly_summary(user, year=None, month=None):
    """
    Calculate monthly summary: total income, total expenses, and net balance.
    
    Args:
        user: Django User object
        year: Year (defaults to current year)
        month: Month (defaults to current month)
    
    Returns:
        Dictionary with summary data
    """
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month

    incomes = Income.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    )
    expenses = Expense.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    )

    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0
    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0
    net_balance = total_income - total_expense

    return {
        'year': year,
        'month': month,
        'total_income': float(total_income),
        'total_expense': float(total_expense),
        'net_balance': float(net_balance),
        'income_count': incomes.count(),
        'expense_count': expenses.count(),
    }


def get_category_breakdown(user, year=None, month=None):
    """
    Calculate expense breakdown by category.
    
    Args:
        user: Django User object
        year: Year (defaults to current year)
        month: Month (defaults to current month)
    
    Returns:
        Dictionary with breakdown data
    """
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month

    expenses = Expense.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    )

    breakdown = expenses.values('category__name', 'category__id').annotate(
        total=Sum('amount'),
        count=Sum('id')
    ).order_by('-total')

    return {
        'year': year,
        'month': month,
        'breakdown': list(breakdown),
        'total_expenses': float(expenses.aggregate(total=Sum('amount'))['total'] or 0),
    }


def get_budget_status(user):
    """
    Get the status of all budgets for the user (current month).
    
    Args:
        user: Django User object
    
    Returns:
        Dictionary with budget status data
    """
    today = date.today()
    budgets = Budget.objects.filter(
        user=user,
        start_date__lte=today,
        end_date__gte=today
    )

    budget_status = []
    for budget in budgets:
        expenses = Expense.objects.filter(
            user=user,
            category=budget.category,
            date__gte=budget.start_date,
            date__lte=budget.end_date
        )
        spent = expenses.aggregate(total=Sum('amount'))['total'] or 0
        remaining = budget.limit_amount - spent
        percentage = (spent / budget.limit_amount * 100) if budget.limit_amount > 0 else 0

        budget_status.append({
            'id': budget.id,
            'category': budget.category.name,
            'limit_amount': float(budget.limit_amount),
            'spent': float(spent),
            'remaining': float(remaining),
            'percentage': round(percentage, 2),
            'exceeded': spent > budget.limit_amount,
        })

    return {
        'current_date': today.isoformat(),
        'budgets': budget_status,
        'total_active_budgets': len(budget_status),
        'exceeded_count': sum(1 for b in budget_status if b['exceeded']),
    }


def get_spending_projection(user, category=None):
    """
    Project spending for the rest of the month based on current pace.
    
    Args:
        user: Django User object
        category: Optional Category object (if None, projects all expenses)
    
    Returns:
        Dictionary with projection data
    """
    today = date.today()
    days_in_month = (date(today.year, today.month, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    days_passed = today.day
    days_remaining = days_in_month.day - today.day

    expense_filter = {
        'user': user,
        'date__year': today.year,
        'date__month': today.month,
    }
    if category:
        expense_filter['category'] = category

    current_expenses = Expense.objects.filter(**expense_filter)
    current_spent = current_expenses.aggregate(total=Sum('amount'))['total'] or 0

    # Calculate daily average
    daily_average = current_spent / days_passed if days_passed > 0 else 0
    projected_end_of_month = current_spent + (daily_average * days_remaining)

    return {
        'current_date': today.isoformat(),
        'days_passed': days_passed,
        'days_remaining': days_remaining,
        'current_spent': float(current_spent),
        'daily_average': round(float(daily_average), 2),
        'projected_end_of_month': round(float(projected_end_of_month), 2),
        'category': category.name if category else 'All',
    }
