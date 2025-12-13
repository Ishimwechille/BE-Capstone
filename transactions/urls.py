"""Transactions app URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transactions import views

router = DefaultRouter()
router.register(r'income', views.IncomeViewSet, basename='income')
router.register(r'expenses', views.ExpenseViewSet, basename='expense')

urlpatterns = [
    path('', include(router.urls)),
]
