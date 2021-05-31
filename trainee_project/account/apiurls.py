from .apiviews import Logout, RegistartionView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_pair'),
    path('logout/', Logout.as_view(), name='auth_logout'),
    path('register/', RegistartionView.as_view(), name='auth_register'),
]
