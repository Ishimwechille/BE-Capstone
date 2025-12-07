from rest_framework import serializers
from .models import Expense, Income
from rest_framework import serializers
from .models import Category, Budget, Goal
from rest_framework import viewsets
from .models import Category, Budget, Goal
from .serializers import CategorySerializer, BudgetSerializer, GoalSerializer

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = "__all__"
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = "__all__"

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = "__all__"
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

