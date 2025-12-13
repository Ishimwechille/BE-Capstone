"""
Django management command to check budgets and generate alerts.

This command should be run daily via a Cron job or scheduler.
It checks all active budgets and generates alerts based on spending patterns.

Usage:
    python manage.py check_budgets
    python manage.py check_budgets --user_id=1
    python manage.py check_budgets --send-email
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import date, timedelta
from budgets.models import Budget, Goal
from transactions.models import Expense
from reports.models import Alert
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Check budgets and generate alerts for spending patterns'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user_id',
            type=int,
            help='Process only a specific user (by ID)'
        )
        parser.add_argument(
            '--send-email',
            action='store_true',
            help='Send email notifications to users'
        )

    def handle(self, *args, **options):
        user_id = options.get('user_id')
        send_email = options.get('send_email', False)

        # Get users to process
        if user_id:
            users = User.objects.filter(id=user_id)
        else:
            users = User.objects.all()

        alert_count = 0
        today = date.today()

        for user in users:
            self.stdout.write(f'Processing user: {user.username}')

            # Check budgets
            budgets = Budget.objects.filter(
                user=user,
                start_date__lte=today,
                end_date__gte=today
            )

            for budget in budgets:
                # Calculate current spending
                current_spending = Expense.objects.filter(
                    user=user,
                    category=budget.category,
                    date__gte=budget.start_date,
                    date__lte=budget.end_date
                ).aggregate(total=Sum('amount'))['total'] or 0

                remaining_budget = budget.limit_amount - current_spending
                spending_percentage = (current_spending / budget.limit_amount * 100) if budget.limit_amount > 0 else 0

                # Calculate days remaining
                days_remaining = (budget.end_date - today).days
                days_elapsed = (today - budget.start_date).days + 1
                total_days = (budget.end_date - budget.start_date).days + 1

                # Calculate daily pace
                daily_limit = budget.limit_amount / total_days if total_days > 0 else 0
                daily_spent = current_spending / days_elapsed if days_elapsed > 0 else 0

                # Generate alerts based on spending patterns
                alert_generated = False

                # DANGER ALERT: Exceeding budget
                if current_spending > budget.limit_amount:
                    title = f'⚠️ Budget Exceeded: {budget.category.name}'
                    message = (
                        f'You have exceeded your budget for {budget.category.name}!\n'
                        f'Limit: ${budget.limit_amount:.2f}\n'
                        f'Current Spending: ${current_spending:.2f}\n'
                        f'Overspent by: ${current_spending - budget.limit_amount:.2f}'
                    )
                    self._create_alert(user, title, message, 'danger', budget.category.name)
                    alert_count += 1
                    alert_generated = True
                    self.stdout.write(
                        self.style.WARNING(f'  - DANGER: {budget.category.name} budget exceeded')
                    )

                # WARNING ALERT: On pace to exceed budget
                elif spending_percentage >= 75 and not alert_generated:
                    remaining_days = days_remaining
                    projected_daily_spend = daily_spent
                    projected_end_spending = current_spending + (projected_daily_spend * remaining_days)

                    if projected_end_spending > budget.limit_amount:
                        title = f'⚠️ Budget At Risk: {budget.category.name}'
                        message = (
                            f'At your current spending pace, you will exceed your '
                            f'{budget.category.name} budget by the end of the month.\n'
                            f'Limit: ${budget.limit_amount:.2f}\n'
                            f'Current Spending: ${current_spending:.2f} ({spending_percentage:.1f}%)\n'
                            f'Projected End: ${projected_end_spending:.2f}\n'
                            f'Days Remaining: {remaining_days}'
                        )
                        self._create_alert(user, title, message, 'danger', budget.category.name)
                        alert_count += 1
                        alert_generated = True
                        self.stdout.write(
                            self.style.WARNING(f'  - WARNING: {budget.category.name} on pace to exceed')
                        )

                # SUCCESS ALERT: On track and under control
                elif spending_percentage <= 50 and not alert_generated:
                    title = f'✅ Budget On Track: {budget.category.name}'
                    message = (
                        f'Great job! You\'re managing your {budget.category.name} budget well.\n'
                        f'Limit: ${budget.limit_amount:.2f}\n'
                        f'Current Spending: ${current_spending:.2f} ({spending_percentage:.1f}%)\n'
                        f'Remaining: ${remaining_budget:.2f}'
                    )
                    self._create_alert(user, title, message, 'success', budget.category.name)
                    alert_count += 1
                    alert_generated = True
                    self.stdout.write(
                        self.style.SUCCESS(f'  - SUCCESS: {budget.category.name} on track')
                    )

                # TIP ALERT: Generic tip based on spending
                elif not alert_generated and days_remaining <= 3 and remaining_budget > 0:
                    title = f'💡 Tip: {budget.category.name} Budget Ending Soon'
                    message = (
                        f'Your {budget.category.name} budget period ends in {days_remaining} day(s).\n'
                        f'You have ${remaining_budget:.2f} remaining.\n'
                        f'Make sure to review your spending for this period.'
                    )
                    self._create_alert(user, title, message, 'tip', budget.category.name)
                    alert_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  - TIP: {budget.category.name} budget ending soon')
                    )

            # Check financial goals
            goals = Goal.objects.filter(user=user, is_completed=False)
            for goal in goals:
                days_until_target = (goal.target_date - today).days
                remaining_needed = goal.target_amount - goal.current_amount

                if remaining_needed <= 0:
                    goal.is_completed = True
                    goal.save()
                    title = f'🎉 Goal Completed: {goal.name}'
                    message = f'Congratulations! You\'ve reached your goal: {goal.name}'
                    self._create_alert(user, title, message, 'success', goal.name)
                    alert_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  - GOAL COMPLETED: {goal.name}')
                    )

                elif days_until_target <= 30 and days_until_target > 0:
                    daily_needed = remaining_needed / days_until_target if days_until_target > 0 else 0
                    title = f'🎯 Goal Deadline Approaching: {goal.name}'
                    message = (
                        f'Your goal "{goal.name}" is due in {days_until_target} day(s).\n'
                        f'Target: ${goal.target_amount:.2f}\n'
                        f'Current: ${goal.current_amount:.2f}\n'
                        f'Remaining: ${remaining_needed:.2f}\n'
                        f'Daily Needed: ${daily_needed:.2f}'
                    )
                    self._create_alert(user, title, message, 'info', goal.name)
                    alert_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  - GOAL REMINDER: {goal.name}')
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Alert check completed! Generated {alert_count} alerts.'
            )
        )

        if send_email:
            self.stdout.write('📧 Email sending not yet implemented')

    def _create_alert(self, user, title, message, alert_type, related_category=None):
        """
        Create an alert if it doesn't already exist today for this category.
        Prevents duplicate alerts for the same category on the same day.
        """
        today = date.today()
        existing_alert = Alert.objects.filter(
            user=user,
            related_category=related_category,
            created_at__date=today,
            alert_type=alert_type
        ).exists()

        if not existing_alert:
            Alert.objects.create(
                user=user,
                title=title,
                message=message,
                alert_type=alert_type,
                related_category=related_category
            )
