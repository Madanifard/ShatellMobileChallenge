from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (LoginAPIView, 
                    RegistrationAPIView, 
                    CSVUploadView, 
                    download_csv, 
                    ListUserInfo)

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('register', RegistrationAPIView.as_view(), name='register'),
    path('uploadFile', CSVUploadView.as_view(), name='upload_csv'),
    path('listUserInfo', ListUserInfo.as_view(), name='list_user_info'),
    path('download_csv/<name_file>', download_csv, name='download_csv'),
]
