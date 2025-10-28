
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import RegisterView,LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view() ,name="register"),
    path('logout/', LogoutView.as_view() ,name="logout"),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-only-only-accesssed-by-admin/', TokenRefreshView.as_view(), name='token_refresh'),
    
]