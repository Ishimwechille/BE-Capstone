"""Users app URL configuration."""
from django.urls import path
from users import views, debug_views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    # Authentication endpoints
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    
    # JWT Token endpoints
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Debug endpoints
    path('debug/no-auth/', debug_views.test_no_auth, name='debug-no-auth'),
    path('debug/with-auth/', debug_views.test_with_auth, name='debug-with-auth'),
    path('debug/token/', debug_views.debug_token, name='debug-token'),
    #home url
    
]
