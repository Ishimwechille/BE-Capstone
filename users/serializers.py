"""Users app serializers."""
from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile - Read and Update."""
    bio = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Short biography of the user (max 500 characters)"
    )
    phone_number = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="User's phone number in E.164 format (e.g., +1234567890)"
    )
    base_currency = serializers.CharField(
        required=False,
        help_text="Base currency for transactions (e.g., USD, EUR, GBP, KES)"
    )

    class Meta:
        model = UserProfile
        fields = ['id', 'bio', 'phone_number', 'base_currency', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User registration and authentication."""
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']
        read_only_fields = ['id', 'profile']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Password must be at least 8 characters long"
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Confirm password - must match password field"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'username': {'help_text': 'Unique username for login (alphanumeric and underscores only)'},
            'email': {'help_text': 'Valid email address for account recovery'},
            'first_name': {'help_text': 'User first name (optional)'},
            'last_name': {'help_text': 'User last name (optional)'},
        }

    def validate(self, data):
        """Validate that passwords match."""
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        """Create and return a user instance."""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField(
        help_text="Your unique username"
    )
    password = serializers.CharField(
        write_only=True,
        help_text="Your account password"
    )

class UpdateUserSerializer(serializers.Serializer):
    """Serializer for updating user information and profile."""
    email = serializers.EmailField(
        required=False,
        help_text="User's email address"
    )
    first_name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=150,
        help_text="User's first name"
    )
    last_name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=150,
        help_text="User's last name"
    )
    bio = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Short biography"
    )
    phone_number = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Phone number"
    )
    base_currency = serializers.CharField(
        required=False,
        help_text="Base currency for transactions"
    )

    def update(self, instance, validated_data):
        """Update user and profile data."""
        # Extract profile fields from validated data
        bio = validated_data.pop('bio', None)
        phone_number = validated_data.pop('phone_number', None)
        base_currency = validated_data.pop('base_currency', None)
        
        # Update user fields
        for attr, value in validated_data.items():
            if value is not None and hasattr(instance, attr):
                setattr(instance, attr, value)
        instance.save()
        
        # Update profile fields if provided
        profile = instance.userprofile
        if bio is not None:
            profile.bio = bio
        if phone_number is not None:
            profile.phone_number = phone_number
        if base_currency is not None:
            profile.base_currency = base_currency
        profile.save()
        
        return instance
