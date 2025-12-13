"""Budgets app serializers."""
from rest_framework import serializers
from budgets.models import Category, Budget, Goal
from django.db.models import Sum
from datetime import datetime


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category."""
    name = serializers.CharField(
        max_length=100,
        help_text="Category name (e.g., Food, Transport, Salary)"
    )
    type = serializers.CharField(
        max_length=10,
        help_text="Category type: 'income' or 'expense'"
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Category description"
    )
    icon = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Icon name or emoji for the category"
    )

    class Meta:
        model = Category
        fields = [
            'id', 'user', 'name', 'type', 'description',
            'icon', 'is_default', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class BudgetSerializer(serializers.ModelSerializer):
    """Serializer for Budget."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    spent_amount = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()
    limit_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Budget limit amount for the period"
    )
    start_date = serializers.DateField(
        help_text="Budget period start date (YYYY-MM-DD)"
    )
    end_date = serializers.DateField(
        help_text="Budget period end date (YYYY-MM-DD)"
    )

    class Meta:
        model = Budget
        fields = [
            'id', 'user', 'category', 'category_name', 'limit_amount',
            'spent_amount', 'remaining_amount', 'start_date', 'end_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
        extra_kwargs = {
            'category': {'help_text': 'Category ID to set budget for'}
        }

    def get_spent_amount(self, obj):
        """Calculate total spent in this budget period."""
        from transactions.models import Expense
        spent = Expense.objects.filter(
            user=obj.user,
            category=obj.category,
            date__gte=obj.start_date,
            date__lte=obj.end_date
        ).aggregate(total=Sum('amount'))['total'] or 0
        return spent

    def get_remaining_amount(self, obj):
        """Calculate remaining budget."""
        from transactions.models import Expense
        spent = Expense.objects.filter(
            user=obj.user,
            category=obj.category,
            date__gte=obj.start_date,
            date__lte=obj.end_date
        ).aggregate(total=Sum('amount'))['total'] or 0
        return float(obj.limit_amount) - float(spent)


class GoalSerializer(serializers.ModelSerializer):
    """Serializer for Goal."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()
    name = serializers.CharField(
        max_length=200,
        help_text="Goal name (e.g., Buy a car, Emergency fund)"
    )
    target_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Target amount to save"
    )
    current_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Current amount saved towards goal"
    )
    target_date = serializers.DateField(
        help_text="Target completion date (YYYY-MM-DD)"
    )

    class Meta:
        model = Goal
        fields = [
            'id', 'user', 'name', 'description', 'target_amount',
            'current_amount', 'target_date', 'category', 'category_name',
            'is_completed', 'progress_percentage', 'remaining_amount',
            'days_remaining', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
        extra_kwargs = {
            'category': {'help_text': 'Category ID associated with goal (optional)'},
            'description': {'help_text': 'Goal description and details'}
        }

    def get_progress_percentage(self, obj):
        """Get progress percentage."""
        return obj.progress_percentage

    def get_remaining_amount(self, obj):
        """Get remaining amount."""
        return obj.remaining_amount

    def get_days_remaining(self, obj):
        """Calculate days remaining until target date."""
        from datetime import date
        today = date.today()
        if obj.target_date > today:
            return (obj.target_date - today).days
        return 0
