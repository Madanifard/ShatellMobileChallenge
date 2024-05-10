from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import (LoginAPIView, 
                    RegistrationAPIView, 
                    CSVUploadView, 
                    download_csv, 
                    ListUserInfo)


schema_view = get_schema_view(
    openapi.Info(
        title="SHATELL MOBILE API TEST",
        default_version='v1',
        description="API Documentation",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="amadanifard@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('token', TokenObtainPairView.as_view(), name='token_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('register', RegistrationAPIView.as_view(), name='register'),
    path('uploadFile', CSVUploadView.as_view(), name='upload_csv'),
    path('listUserInfo', ListUserInfo.as_view(), name='list_user_info'),
    path('download_csv/<name_file>', download_csv, name='download_csv'),
]
