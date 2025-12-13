"""Management command to create default categories for all users."""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from budgets.models import Category


class Command(BaseCommand):
    help = 'Create default categories for all users'

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

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=int,
            help='User ID to create categories for (if not specified, creates for all users)'
        )

    def handle(self, *args, **options):
        user_id = options.get('user')
        
        if user_id:
            users = User.objects.filter(id=user_id)
            if not users.exists():
                self.stdout.write(self.style.ERROR(f'User with ID {user_id} not found'))
                return
        else:
            users = User.objects.all()

        total_created = 0

        for user in users:
            created_count = self.create_categories_for_user(user)
            total_created += created_count
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created {created_count} categories for user: {user.username}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(f'\nTotal categories created: {total_created}')
        )

    def create_categories_for_user(self, user):
        """Create default categories for a specific user."""
        created_count = 0

        # Create income categories
        for category in self.DEFAULT_INCOME_CATEGORIES:
            _, created = Category.objects.get_or_create(
                user=user,
                name=category['name'],
                type='income',
                defaults={'icon': category.get('icon', '💰')}
            )
            if created:
                created_count += 1

        # Create expense categories
        for category in self.DEFAULT_EXPENSE_CATEGORIES:
            _, created = Category.objects.get_or_create(
                user=user,
                name=category['name'],
                type='expense',
                defaults={'icon': category.get('icon', '📌')}
            )
            if created:
                created_count += 1

        return created_count
