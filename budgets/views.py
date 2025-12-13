"""Budgets app views."""
import logging
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from budgets.models import Category, Budget, Goal
from budgets.serializers import CategorySerializer, BudgetSerializer, GoalSerializer

logger = logging.getLogger(__name__)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing transaction categories.
    
    Provides CRUD operations for income and expense categories. Users can create
    custom categories or use default categories provided by the system.
    
    List: GET /api/categories/ - Get all categories
    Create: POST /api/categories/ - Create new category
    Retrieve: GET /api/categories/{id}/ - Get specific category
    Update: PUT /api/categories/{id}/ - Update category
    Delete: DELETE /api/categories/{id}/ - Delete category
    
    Filters: type (income/expense), is_default
    Search: name
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type', 'is_default']
    search_fields = ['name']

    def get_queryset(self):
        """Return user's categories and default categories."""
        user = self.request.user
        logger.info(f"📂 CategoryViewSet.get_queryset() called")
        logger.info(f"   User: {user}")
        logger.info(f"   Is Authenticated: {user.is_authenticated}")
        logger.info(f"   User Type: {type(user)}")
        
        if not user.is_authenticated:
            logger.warning(f"   ⚠️ User is not authenticated!")
            return Category.objects.none()
        
        queryset = Category.objects.filter(
            models.Q(user=user) | models.Q(user__isnull=True)
        ).distinct()
        logger.info(f"   Found {queryset.count()} categories")
        return queryset

    def perform_create(self, serializer):
        """Set the user when creating a category."""
        serializer.save(user=self.request.user)


class BudgetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing spending budgets.
    
    Provides CRUD operations for budgets with automatic spent amount calculation and
    exceeded budget detection.
    
    List: GET /api/budgets/ - Get all budgets
    Create: POST /api/budgets/ - Create new budget
    Retrieve: GET /api/budgets/{id}/ - Get specific budget
    Update: PUT /api/budgets/{id}/ - Update budget
    Delete: DELETE /api/budgets/{id}/ - Delete budget
    
    Actions:
    - current_month: GET /api/budgets/current_month/ - Get active budgets for current month
    - exceeded: GET /api/budgets/exceeded/ - Get budgets that exceeded limit
    
    Filters: category, start_date, end_date
    Ordering: start_date, limit_amount
    """
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'start_date', 'end_date']
    ordering_fields = ['start_date', 'limit_amount']
    ordering = ['-start_date']

    def get_queryset(self):
        """Return only the current user's budgets."""
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user when creating a budget."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def current_month(self, request):
        """
        Get budgets active for the current month.
        
        Query Parameters:
        - year: Year (default: current year)
        - month: Month 1-12 (default: current month)
        
        Returns: List of budgets active in the specified period
        """
        from datetime import datetime, date
        today = date.today()
        year = request.query_params.get('year', today.year)
        month = request.query_params.get('month', today.month)

        from datetime import date as date_cls
        first_day = date_cls(int(year), int(month), 1)
        if int(month) == 12:
            last_day = date_cls(int(year) + 1, 1, 1)
        else:
            last_day = date_cls(int(year), int(month) + 1, 1)

        budgets = self.get_queryset().filter(
            start_date__lte=first_day,
            end_date__gte=first_day
        )
        return Response(BudgetSerializer(budgets, many=True).data)

    @action(detail=False, methods=['get'])
    def exceeded(self, request):
        """
        Get budgets that have been exceeded.
        
        Returns: List of budgets where spent amount exceeds the limit
        """
        from django.db.models import Sum
        from transactions.models import Expense

        exceeded_budgets = []
        for budget in self.get_queryset():
            spent = Expense.objects.filter(
                user=request.user,
                category=budget.category,
                date__gte=budget.start_date,
                date__lte=budget.end_date
            ).aggregate(total=Sum('amount'))['total'] or 0

            if spent > budget.limit_amount:
                exceeded_budgets.append(budget)

        return Response(BudgetSerializer(exceeded_budgets, many=True).data)


class GoalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing financial goals.
    
    Provides CRUD operations for savings goals with progress tracking and completion marking.
    
    List: GET /api/goals/ - Get all goals
    Create: POST /api/goals/ - Create new goal
    Retrieve: GET /api/goals/{id}/ - Get specific goal
    Update: PUT /api/goals/{id}/ - Update goal
    Delete: DELETE /api/goals/{id}/ - Delete goal
    
    Actions:
    - mark_completed: POST /api/goals/{id}/mark_completed/ - Mark goal as complete
    - update_progress: POST /api/goals/{id}/update_progress/ - Update progress amount
    
    Filters: category, is_completed
    Ordering: target_date, target_amount
    """
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'is_completed']
    ordering_fields = ['target_date', 'target_amount']
    ordering = ['target_date']

    def get_queryset(self):
        """Return only the current user's goals."""
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user when creating a goal."""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """
        Mark a goal as completed.
        
        Sets the is_completed flag to True for the goal.
        """
        goal = self.get_object()
        goal.is_completed = True
        goal.save()
        return Response(GoalSerializer(goal).data)

    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """
        Update the current progress amount towards the goal.
        
        Request body:
        - current_amount: New current amount saved
        """
        goal = self.get_object()
        current_amount = request.data.get('current_amount')
        if current_amount is not None:
            goal.current_amount = current_amount
            if goal.current_amount >= goal.target_amount:
                goal.is_completed = True
            goal.save()
        return Response(GoalSerializer(goal).data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active (not completed) goals."""
        active_goals = self.get_queryset().filter(is_completed=False)
        return Response(GoalSerializer(active_goals, many=True).data)
