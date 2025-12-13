"""Transactions app serializers."""
from rest_framework import serializers
from transactions.models import Income, Expense
from django.db.models import Sum
from decimal import Decimal


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
        required=False,
        allow_null=True,
        help_text="Original transaction amount"
    )
    currency = serializers.CharField(
        max_length=3,
        required=False,
        default='USD',
        help_text="Currency code (e.g., USD, EUR, GBP, KES)"
    )
    exchange_rate = serializers.DecimalField(
        max_digits=10,
        decimal_places=4,
        required=False,
        default=1.0,
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

    def validate_amount(self, value):
        """Validate that amount is positive."""
        if value <= 0:
            raise serializers.ValidationError("Expense amount must be greater than 0.")
        return value

    def validate(self, data):
        """Validate that expense doesn't exceed user's balance."""
        # Get the user from the view context
        user = self.context['request'].user if 'request' in self.context else None
        
        if not user:
            raise serializers.ValidationError("User context is required.")
        
        # Calculate current balance
        total_income = Income.objects.filter(user=user).aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0')
        
        total_expenses = Expense.objects.filter(user=user).aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0')
        
        current_balance = total_income - total_expenses
        expense_amount = data.get('amount', Decimal('0'))
        
        # Check if new expense would exceed balance
        if expense_amount > current_balance:
            raise serializers.ValidationError(
                f"Insufficient balance. Your current balance is ${current_balance:.2f}, "
                f"but you're trying to spend ${expense_amount:.2f}. "
                f"Maximum you can spend is ${current_balance:.2f}."
            )
        
        return data

    def create(self, validated_data):
        """Create expense and set original_amount to amount if not provided."""
        if 'original_amount' not in validated_data or validated_data['original_amount'] is None:
            validated_data['original_amount'] = validated_data['amount']
        return super().create(validated_data)