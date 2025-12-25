"""
Home view for API welcome message
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    """
    Home endpoint - Welcome message for Sentinel Tracker API
    """
    return Response({
        'message': 'Welcome to Sentinel Tracker API',
        'description': 'Advanced Expense & Goal Manager - Personal Finance API',
        'version': '1.0.0',
        'status': 'Production',
        'environment': 'Production',
        'documentation': {
            'swagger': 'http://localhost:8000/api/docs/',
            'redoc': 'http://localhost:8000/api/redoc/',
            'schema': 'http://localhost:8000/api/schema/',
        },
        'endpoints': {
            'authentication': '/api/auth/',
            'transactions': '/api/transactions/',
            'budgets': '/api/budgets/',
            'reports': '/api/reports/',
        },
        'features': [
            'User authentication with JWT',
            'Income & expense tracking',
            'Budget management',
            'Savings goals tracking',
            'Financial reports & analytics',
            'Alert system',
        ],
        'database': 'PostgreSQL',
        'api_version': 'v1.0',
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for monitoring
    """
    return Response({
        'status': 'healthy',
        'message': 'API is running',
        'environment': 'production',
    }, status=status.HTTP_200_OK)
