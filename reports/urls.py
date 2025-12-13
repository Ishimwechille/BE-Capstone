"""Reports app URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reports import views

router = DefaultRouter()
router.register(r'alerts', views.AlertViewSet, basename='alert')
router.register(r'', views.ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]
