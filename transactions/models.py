"""Transactions app models."""
from django.db import models
from django.contrib.auth.models import User
from budgets.models import Category


class Income(models.Model):
    """Income transaction record."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incomes'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Income'
        verbose_name_plural = 'Incomes'

    def __str__(self):
        return f"Income: ${self.amount} on {self.date}"


class Expense(models.Model):
    """Expense transaction record."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    currency = models.CharField(
        max_length=3,
        default='USD',
        help_text='Original currency of the expense'
    )
    original_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Amount in original currency before conversion'
    )
    exchange_rate = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=1.0,
        help_text='Exchange rate used for conversion to base currency'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'

    def __str__(self):
        return f"Expense: ${self.amount} on {self.date}"
