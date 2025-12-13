"""Reports app views."""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from reports.models import Alert
from reports.serializers import AlertSerializer
from reports.logic import (
    get_monthly_summary,
    get_category_breakdown,
    get_budget_status,
    get_spending_projection,
)


class AlertViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing financial alerts.
    
    Provides CRUD operations for alerts with read/unread status tracking.
    Alerts are automatically generated when budgets are exceeded or goals are updated.
    
    List: GET /api/alerts/ - Get all alerts
    Create: POST /api/alerts/ - Create new alert (manual)
    Retrieve: GET /api/alerts/{id}/ - Get specific alert
    Update: PUT /api/alerts/{id}/ - Update alert
    Delete: DELETE /api/alerts/{id}/ - Delete alert
    
    Actions:
    - mark_as_read: POST /api/alerts/{id}/mark_as_read/ - Mark single alert as read
    - mark_all_as_read: POST /api/alerts/mark_all_as_read/ - Mark all alerts as read
    - unread: GET /api/alerts/unread/ - Get all unread alerts
    
    Filters: alert_type, is_read
    Ordering: created_at
    """
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['alert_type', 'is_read']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return only the current user's alerts."""
        return Alert.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user when creating an alert."""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Mark a specific alert as read.
        
        Returns: Updated alert object
        """
        alert = self.get_object()
        alert.is_read = True
        alert.save()
        return Response(AlertSerializer(alert).data)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """
        Mark all unread alerts as read.
        
        Returns: Count of alerts marked as read
        """
        alerts = self.get_queryset().filter(is_read=False)
        alerts.update(is_read=True)
        return Response({
            'message': f'{alerts.count()} alerts marked as read'
        })

    @action(detail=False, methods=['get'])
    def unread(self, request):
        """
        Get all unread alerts for the user.
        
        Returns: Count and list of unread alerts
        """
        unread_alerts = self.get_queryset().filter(is_read=False)
        return Response({
            'count': unread_alerts.count(),
            'alerts': AlertSerializer(unread_alerts, many=True).data
        })


class ReportViewSet(viewsets.ViewSet):
    """
    ViewSet for financial reports and analysis.
    
    Provides various financial analytics including summaries, breakdowns,
    budget status, and spending projections.
    
    Actions:
    - summary: GET /api/reports/summary/?year=2024&month=12 - Monthly financial summary
    - breakdown: GET /api/reports/breakdown/?year=2024&month=12 - Expense breakdown by category
    - budget_status: GET /api/reports/budget_status/ - Status of all active budgets
    - spending_projection: GET /api/reports/spending_projection/?category=ID - Projected spending
    - dashboard: GET /api/reports/dashboard/ - Complete dashboard overview
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get comprehensive monthly financial summary.
        
        Query Parameters:
        - year: Year (default: current year)
        - month: Month 1-12 (default: current month)
        
        Returns: Total income, total expenses, net, and month/year info
        """
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if year:
            year = int(year)
        if month:
            month = int(month)

        summary = get_monthly_summary(request.user, year, month)
        return Response(summary)

    @action(detail=False, methods=['get'])
    def breakdown(self, request):
        """
        Get expense breakdown by category for a specific month.
        
        Query Parameters:
        - year: Year (default: current year)
        - month: Month 1-12 (default: current month)
        
        Returns: Dictionary with each category showing total spent and percentage
        """
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if year:
            year = int(year)
        if month:
            month = int(month)

        breakdown = get_category_breakdown(request.user, year, month)
        return Response(breakdown)

    @action(detail=False, methods=['get'])
    def budget_status(self, request):
        """
        Get current status of all active budgets.
        
        Returns: List of budgets with spent amount, remaining, and percentage
        """
        status_data = get_budget_status(request.user)
        return Response(status_data)

    @action(detail=False, methods=['get'])
    def spending_projection(self, request):
        """
        Get spending projection for the rest of the current month.
        
        Query Parameters:
        - category: Category ID (optional, for specific category projection)
        
        Returns: Projected spending and projected end-of-month balance
        """
        category_id = request.query_params.get('category')
        category = None

        if category_id:
            from budgets.models import Category
            try:
                category = Category.objects.get(id=category_id, user=request.user)
            except Category.DoesNotExist:
                return Response(
                    {'error': 'Category not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

        projection = get_spending_projection(request.user, category)
        return Response(projection)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """
        Get comprehensive dashboard data.
        
        Combines summary, breakdown, and budget status.
        """
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if year:
            year = int(year)
        if month:
            month = int(month)

        summary = get_monthly_summary(request.user, year, month)
        breakdown = get_category_breakdown(request.user, year, month)
        budget_status = get_budget_status(request.user)
        projection = get_spending_projection(request.user)

        return Response({
            'summary': summary,
            'breakdown': breakdown,
            'budget_status': budget_status,
            'spending_projection': projection,
        })
