"""Authentication debugging utilities."""
import logging
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed as JWTAuthenticationFailed

logger = logging.getLogger(__name__)


class DebugJWTAuthentication(JWTAuthentication):
    """JWT Authentication with debug logging."""
    
    def authenticate(self, request):
        """Authenticate with detailed logging."""
        auth = get_authorization_header(request).split()
        
        logger.info(f"🔐 AUTH REQUEST: {request.method} {request.path}")
        logger.info(f"📦 Authorization Header: {auth}")
        
        if not auth:
            logger.warning("⚠️ No authorization header found")
            return None
        
        if len(auth) == 1:
            logger.error("❌ Invalid token header (no credentials)")
            msg = 'Invalid token header. No credentials provided.'
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            logger.error("❌ Invalid token header (too many parts)")
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise AuthenticationFailed(msg)
        
        try:
            auth_type = auth[0].decode()
            token = auth[1].decode()
        except UnicodeDecodeError:
            logger.error("❌ Could not decode auth header")
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise AuthenticationFailed(msg)
        
        logger.info(f"🔑 Token Type: {auth_type}, Token Length: {len(token)}")
        
        if auth_type.lower() != 'bearer':
            logger.error(f"❌ Wrong auth type: {auth_type}")
            msg = f'Invalid token header. Auth type "{auth_type}" is not "Bearer".'
            raise AuthenticationFailed(msg)
        
        try:
            validated_token = self.get_validated_token(token)
            logger.info(f"✅ Token validated successfully for user_id: {validated_token.get('user_id')}")
        except InvalidToken as e:
            logger.error(f"❌ Token validation failed: {e}")
            raise
        except JWTAuthenticationFailed as e:
            logger.error(f"❌ JWT authentication failed: {e}")
            raise
        
        user = self.get_user(validated_token)
        logger.info(f"✅ User authenticated: {user.username} (ID: {user.id})")
        return (user, validated_token)
