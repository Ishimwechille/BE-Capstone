"""Transactions app views."""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from transactions.models import Income, Expense
from transactions.serializers import IncomeSerializer, ExpenseSerializer


class IncomeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing income transactions.
    
    Provides CRUD operations for income records with filtering, search, and monthly summaries.
    
    List: GET /api/incomes/ - Get all income records
    Create: POST /api/incomes/ - Record new income
    Retrieve: GET /api/incomes/{id}/ - Get specific income
    Update: PUT /api/incomes/{id}/ - Update income record
    Delete: DELETE /api/incomes/{id}/ - Delete income record
    
    Actions:
    - by_month: GET /api/incomes/by_month/?year=2024&month=12 - Get monthly summary
    
    Filters: category, date
    Search: description
    Ordering: date, amount, created_at
    """
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'date']
    search_fields = ['description']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        """Return only the current user's incomes."""
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user when creating an income."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def by_month(self, request):
        """
        Get income summary by month.
        
        Query Parameters:
        - year: Year (default: current year)
        - month: Month 1-12 (default: current month)
        
        Returns:
        - year, month, total, count, list of incomes
        """
        from django.db.models import Sum
        from datetime import datetime

        year = request.query_params.get('year', datetime.now().year)
        month = request.query_params.get('month', datetime.now().month)

        incomes = self.get_queryset().filter(date__year=year, date__month=month)
        total = incomes.aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            'year': year,
            'month': month,
            'total': total,
            'count': incomes.count(),
            'incomes': IncomeSerializer(incomes, many=True).data
        })


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing expense transactions.
    
    Provides CRUD operations for expense records with multi-currency support, filtering, and monthly summaries.
    
    List: GET /api/expenses/ - Get all expense records
    Create: POST /api/expenses/ - Record new expense
    Retrieve: GET /api/expenses/{id}/ - Get specific expense
    Update: PUT /api/expenses/{id}/ - Update expense record
    Delete: DELETE /api/expenses/{id}/ - Delete expense record
    
    Actions:
    - by_month: GET /api/expenses/by_month/?year=2024&month=12 - Get monthly summary
    
    Filters: category, date, currency
    Search: description
    Ordering: date, amount, created_at
    
    Multi-currency: Automatically converts to base currency using exchange rate
    """
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'date', 'currency']
    search_fields = ['description']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        """Return only the current user's expenses."""
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user when creating an expense."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def by_month(self, request):
        """
        Get expense summary by month.
        
        Query Parameters:
        - year: Year (default: current year)
        - month: Month 1-12 (default: current month)
        
        Returns:
        - year, month, total, count, list of expenses
        """
        from django.db.models import Sum
        from datetime import datetime

        year = request.query_params.get('year', datetime.now().year)
        month = request.query_params.get('month', datetime.now().month)

        expenses = self.get_queryset().filter(date__year=year, date__month=month)
        total = expenses.aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            'year': year,
            'month': month,
            'total': total,
            'count': expenses.count(),
            'expenses': ExpenseSerializer(expenses, many=True).data
        })

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get expense breakdown by category."""
        from django.db.models import Sum
        from datetime import datetime

        year = request.query_params.get('year', datetime.now().year)
        month = request.query_params.get('month', datetime.now().month)

        expenses = self.get_queryset().filter(date__year=year, date__month=month)
        breakdown = expenses.values('category__name').annotate(
            total=Sum('amount'),
            count=Sum('id')
        ).order_by('-total')

        return Response({
            'year': year,
            'month': month,
            'breakdown': list(breakdown)
        })
