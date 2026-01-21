
from django.urls import path
from .views import RegisterView,LogoutView,VerifyEmailView,ProfileView,ForgotPasswordView,PasswordResetView
import os
from dotenv import load_dotenv
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', RegisterView.as_view() ,name="register"),
    path('logout/', LogoutView.as_view() ,name="logout"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-only-accesssed-by-admin/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/',VerifyEmailView.as_view(),name="email_verify"),
    path('profile/', ProfileView.as_view() ,name="profile"),
    path('profile/password/reset/', PasswordResetView.as_view() ,name="reset_password"),
    path('profile/password/forgot/', ForgotPasswordView.as_view() ,name="forgot_password"),



    
    
]