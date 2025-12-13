"""Users app signals for automatic profile creation."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from users.models import UserProfile


# Default categories to create for new users
DEFAULT_INCOME_CATEGORIES = [
    {'name': 'Salary', 'icon': '💰'},
    {'name': 'Freelance', 'icon': '💻'},
    {'name': 'Investment', 'icon': '📈'},
    {'name': 'Bonus', 'icon': '🎁'},
    {'name': 'Other Income', 'icon': '✅'},
]

DEFAULT_EXPENSE_CATEGORIES = [
    {'name': 'Groceries', 'icon': '🛒'},
    {'name': 'Transport', 'icon': '🚗'},
    {'name': 'Utilities', 'icon': '💡'},
    {'name': 'Entertainment', 'icon': '🎮'},
    {'name': 'Healthcare', 'icon': '🏥'},
    {'name': 'Dining', 'icon': '🍽️'},
    {'name': 'Shopping', 'icon': '🛍️'},
    {'name': 'Education', 'icon': '📚'},
    {'name': 'Insurance', 'icon': '🛡️'},
    {'name': 'Other Expense', 'icon': '📌'},
]


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile and Token when a new User is created."""
    if created:
        UserProfile.objects.create(user=instance)
        Token.objects.create(user=instance)
        
        # Create default categories for the user
        create_default_categories(instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the user profile when the user is saved."""
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)


def create_default_categories(user):
    """Create default income and expense categories for a new user."""
    from budgets.models import Category
    
    # Create income categories
    for category in DEFAULT_INCOME_CATEGORIES:
        Category.objects.get_or_create(
            user=user,
            name=category['name'],
            type='income',
            defaults={'icon': category.get('icon', '💰')}
        )
    
    # Create expense categories
    for category in DEFAULT_EXPENSE_CATEGORIES:
        Category.objects.get_or_create(
            user=user,
            name=category['name'],
            type='expense',
            defaults={'icon': category.get('icon', '📌')}
        )
