"""Debug views for testing token authentication."""
import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import get_authorization_header

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def test_no_auth(request):
    """Test endpoint that doesn't require authentication."""
    auth = get_authorization_header(request)
    return Response({
        'message': 'This endpoint requires no authentication',
        'received_auth_header': auth.decode('utf-8') if auth else None,
        'timestamp': str(__import__('django.utils.timezone', fromlist=['now']).now())
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_with_auth(request):
    """Test endpoint that requires authentication."""
    return Response({
        'message': 'You are authenticated!',
        'user': str(request.user),
        'user_id': request.user.id,
        'timestamp': str(__import__('django.utils.timezone', fromlist=['now']).now())
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def debug_token(request):
    """Debug endpoint to verify token format."""
    auth = get_authorization_header(request)
    token = request.data.get('token', '')
    
    logger.info(f"🔐 Debug Token Request:")
    logger.info(f"   Auth Header: {auth}")
    logger.info(f"   Token (raw): {token}")
    logger.info(f"   Token Length: {len(token)}")
    
    if auth:
        auth_parts = auth.split()
        logger.info(f"   Auth Type: {auth_parts[0].decode() if len(auth_parts) > 0 else 'NONE'}")
        logger.info(f"   Auth Token Length: {len(auth_parts[1]) if len(auth_parts) > 1 else 0}")
    
    return Response({
        'message': 'Token debug info logged',
        'auth_header_received': bool(auth),
        'body_token_received': bool(token)
    })
