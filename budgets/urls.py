"""Budgets app URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from budgets import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'budgets', views.BudgetViewSet, basename='budget')
router.register(r'goals', views.GoalViewSet, basename='goal')

urlpatterns = [
    path('', include(router.urls)),
]
