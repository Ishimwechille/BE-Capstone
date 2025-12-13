"""Custom exception handler for detailed error responses."""
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Custom exception handler with detailed logging."""
    response = exception_handler(exc, context)
    
    request = context.get('request')
    method = request.method if request else 'UNKNOWN'
    path = request.path if request else 'UNKNOWN'
    
    if response is None:
        logger.error(f"❌ Unhandled exception in {method} {path}: {exc}")
        return Response(
            {'error': str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    status_code = response.status_code
    if status_code >= 400:
        logger.warning(f"⚠️ {status_code} {method} {path}")
        logger.warning(f"   Exception: {exc}")
        if response.data:
            logger.warning(f"   Response: {response.data}")
    
    return response
