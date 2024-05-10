from django.urls import path
from .views import LoginView, RegisterView, UserInfoView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('userInfo', UserInfoView.as_view(), name='panel_user_info')
]
