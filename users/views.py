"""Users app views."""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import RegisterSerializer, LoginSerializer, UserSerializer, UpdateUserSerializer


@extend_schema(
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            description="User successfully registered with JWT tokens",
            response=UserSerializer
        ),
        400: OpenApiResponse(
            description="Validation error - invalid input data"
        )
    },
    description="Register a new user account and receive JWT tokens (access + refresh)"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user account.
    
    Create a new user account with username, email, password, and optional name fields.
    A UserProfile and JWT tokens (access and refresh) are automatically created.
    
    Request Body:
    {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "securepass123",
        "password2": "securepass123",
        "first_name": "John",
        "last_name": "Doe"
    }
    
    Returns:
    - user: Created user object with profile
    - access: JWT access token (valid for 15 minutes)
    - refresh: JWT refresh token (valid for 7 days)
    
    Status Codes:
    - 201: User created successfully
    - 400: Validation error (password mismatch, username exists, etc.)
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            description="User authenticated successfully with JWT tokens",
            response=UserSerializer
        ),
        401: OpenApiResponse(
            description="Authentication failed - invalid credentials"
        ),
        400: OpenApiResponse(
            description="Validation error - missing required fields"
        )
    },
    description="Authenticate user with username and password, receive JWT tokens"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Authenticate user and obtain JWT tokens.
    
    Validates username and password. On successful authentication, returns the user
    object, access token, and refresh token.
    
    Request Body:
    {
        "username": "john_doe",
        "password": "securepass123"
    }
    
    Returns:
    - user: Authenticated user object
    - access: JWT access token (valid for 15 minutes)
    - refresh: JWT refresh token (valid for 7 days)
    
    Status Codes:
    - 200: Authentication successful
    - 401: Invalid credentials (wrong username or password)
    - 400: Validation error (missing username or password)
    
    Usage:
    Use the 'access' token in the Authorization header for API requests:
    Authorization: Bearer <access_token>
    
    When access token expires, use refresh token to get a new access token
    via POST /api/auth/token/refresh/
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=None,
    responses={
        200: OpenApiResponse(
            description="User profile retrieved successfully",
            response=UserSerializer
        ),
        401: OpenApiResponse(
            description="Unauthorized - invalid or missing JWT token"
        )
    },
    description="Retrieve current user's profile information"
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Retrieve the authenticated user's profile.
    
    Get detailed information about the currently authenticated user including
    their profile settings, username, email, and name fields.
    
    Authentication: Required (JWT Bearer token)
    
    Request Body: Not applicable (GET request)
    
    Returns:
    - User object with all profile information
    
    Status Codes:
    - 200: Profile retrieved successfully
    - 401: Unauthorized - token invalid or missing
    """
    user = request.user
    return Response(UserSerializer(user).data)


@extend_schema(
    request=None,
    responses={
        200: OpenApiResponse(
            description="User logged out successfully"
        ),
        401: OpenApiResponse(
            description="Unauthorized - invalid or missing JWT token"
        )
    },
    description="Logout authenticated user (blacklist their refresh token)"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout the authenticated user.
    
    Invalidates the user's refresh token by blacklisting it. The access token
    will continue to work until it expires, but cannot be refreshed.
    
    Authentication: Required (JWT Bearer token)
    
    Request Body: Empty (no parameters needed)
    
    Returns:
    - message: Success confirmation
    
    Status Codes:
    - 200: Successfully logged out
    - 401: Unauthorized - token invalid or missing
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': 'Logout failed'},
            status=status.HTTP_400_BAD_REQUEST
        )

@extend_schema(
    request=UpdateUserSerializer,
    responses={
        200: OpenApiResponse(
            description="User profile updated successfully",
            response=UserSerializer
        ),
        400: OpenApiResponse(
            description="Validation error - invalid input data"
        ),
        401: OpenApiResponse(
            description="Unauthorized - invalid or missing JWT token"
        )
    },
    description="Update authenticated user's profile information"
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update the authenticated user's profile.
    
    Update user information including email, name, biography, phone number,
    and base currency for transactions.
    
    Authentication: Required (JWT Bearer token)
    
    Request Body (all fields optional):
    {
        "email": "newemail@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "I love managing my finances",
        "phone_number": "+1234567890",
        "base_currency": "USD"
    }
    
    Returns:
    - Updated user object with profile information
    
    Status Codes:
    - 200: Profile updated successfully
    - 400: Validation error (invalid email, etc.)
    - 401: Unauthorized - token invalid or missing
    """
    user = request.user
    serializer = UpdateUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




