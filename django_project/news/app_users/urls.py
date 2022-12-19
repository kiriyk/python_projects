from django.urls import path
from app_users.views import *

urlpatterns = [
    path('login/', NewLoginView.as_view(), name='login'),
    path('', MainPage.as_view(), name='main-page'),
    path('logout/', NewLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('users-verify/', UsersVerify.as_view(), name='users-verify'),
    path('users-verify-edit/<int:profile_id>/', VerifyUpdateView.as_view(), name='users-verify-edit'),
]
