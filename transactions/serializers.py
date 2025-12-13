"""Transactions app serializers."""
from rest_framework import serializers
from transactions.models import Income, Expense


class IncomeSerializer(serializers.ModelSerializer):
    """Serializer for Income transactions."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Income amount (must be positive)"
    )
    date = serializers.DateField(
        help_text="Transaction date (YYYY-MM-DD format)"
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Description of the income source"
    )

    class Meta:
        model = Income
        fields = [
            'id', 'user', 'category', 'category_name', 'amount',
            'date', 'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
        extra_kwargs = {
            'category': {'help_text': 'Income category ID (e.g., Salary, Bonus, Investment)'}
        }


class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for Expense transactions."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Converted amount in base currency"
    )
    original_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Original transaction amount"
    )
    currency = serializers.CharField(
        max_length=3,
        help_text="Currency code (e.g., USD, EUR, GBP, KES)"
    )
    exchange_rate = serializers.DecimalField(
        max_digits=10,
        decimal_places=4,
        help_text="Exchange rate used for conversion (auto-calculated if not provided)"
    )
    date = serializers.DateField(
        help_text="Transaction date (YYYY-MM-DD format)"
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Description of the expense"
    )

    class Meta:
        model = Expense
        fields = [
            'id', 'user', 'category', 'category_name', 'amount',
            'date', 'description', 'currency', 'original_amount',
            'exchange_rate', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
        extra_kwargs = {
            'category': {'help_text': 'Expense category ID (e.g., Food, Transport, Utilities)'}
        }
