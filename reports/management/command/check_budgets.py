from django.core.management.base import BaseCommand
from budgets.models import Budget
from transactions.models import Expense

class Command(BaseCommand):
    help = "Check budget limits and trigger alerts"

    def handle(self, *args, **kwargs):
        for budget in Budget.objects.all():
            spent = sum(
                expense.amount
                for expense in Expense.objects.filter(
                    user=budget.user,
                    category=budget.category.name
                )
            )

            if spent > budget.limit * 0.8:
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠ {budget.user} is close to exceeding {budget.category} budget!"
                    )
                )
