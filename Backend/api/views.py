from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializer import LoginSerializer, RegistrationSerializer, UserInfoSerializer
from django.http import HttpResponse
from django.urls import reverse
from rest_framework.decorators import schema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .lib import (read_csv_file, 
                  create_csv_file, 
                  output, 
                  convert_error_to_str, 
                  response_download_csv, 
                  insert_user_info, 
                  list_user_info)


class LoginAPIView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: "Success response",
            400: "Bad request response",
            401: "Unauthorized response"
        }
    )
    def post(self, request):
        """
        Log in a user.

        Authenticate user with provided credentials.

        Returns:
        - 200: Success response
        - 400: Bad request response
        - 401: Unauthorized response
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response(output(message="success", 
                                       data={
                                           'refresh': str(refresh),
                                           'access': str(refresh.access_token),
                                           }
                                        ),
                                status=status.HTTP_200_OK)
            else:
                return Response(output(message='error', 
                                       errors=['Invalid credentials']),
                                status=status.HTTP_401_UNAUTHORIZED)
        return Response(output(message='error', 
                               errors=serializer.errors), 
                        status=status.HTTP_400_BAD_REQUEST) 


class RegistrationAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            201: "Created response",
            400: "Bad request response"
        }
    )
    def post(self, request):
        """
        Register a new user.

        Create a new user with Email and Password.

        Returns:
        - 201: Created response
        - 400: Bad request response
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(output(message="success", 
                                   data=serializer.data), 
                            status=status.HTTP_201_CREATED)
        return Response(output(message="Error", 
                               errors=serializer.errors), 
                        status=status.HTTP_400_BAD_REQUEST)


class CSVUploadView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['file_base64'],
            properties={
                'file_base64': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: "Success response",
            400: "Bad request response",
            500: "Internal server error response"
        },
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                description='Bearer token for authentication'
            ),
        ]
    )
    def post(self, request):
        """
        Upload a CSV file.

        Read and process the CSV file data. NOT: csv_file is Base 64 string

        Returns:
        - 200: Success response
        - 400: Bad request response
        - 500: Internal server error response
        """
        file_obj = request.data['file_base64']
        result_read, content_file = read_csv_file(file_obj)
        if not result_read:
            return Response(output(message='Have Error',
                                    errors=['File format not supported']),
                                    status=status.HTTP_400_BAD_REQUEST)
        
        if not content_file:
            return Response(output(message='Have Error',
                                    errors=['file is empty']), 
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            invalid_data = []
            valid_data = []
            counter_failed = 0
            counter_success = 0
            url_download_file = ''
            for item in content_file:
                serializer = UserInfoSerializer(data=item)
                if serializer.is_valid():
                    valid_data.append({
                        'email': item['email'],
                        'national_id': item['national_id'],
                    })
                else:
                    counter_failed += 1
                    invalid_data.append({
                        'email': item['email'],
                        'national_id': item['national_id'],
                        'message': convert_error_to_str(serializer.errors),
                    })

            if valid_data:
                success, failed , failed_list = insert_user_info(valid_data)
                counter_success += success
                counter_failed += failed
                if failed_list:
                    [invalid_data.append(item) for item in failed_list]
            
            if invalid_data:
                name_file = create_csv_file(invalid_data)
                base_url = request.build_absolute_uri()
                url_download_file = base_url + reverse('download_csv', kwargs={'name_file': name_file})

            return Response(output(
                message='result operation',
                data={
                    'success': counter_success,
                    'failed': counter_failed,
                    'url_file_failed': url_download_file
                }
            ), status=status.HTTP_200_OK)
               
        except Exception as e:
            return Response(output(
                message='have Internal Error',
                errors=str(e)
            ), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListUserInfo(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: "Success response"
        },
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                description='Bearer token for authentication'
            ),
        ]
    )
    def get(self, request):
        """
        Retrieve a list of user info.

        Returns:
        - 200: Success response
        """
        user_info_list = list_user_info()
        serializer = UserInfoSerializer(data=user_info_list, many=True)
        serializer.is_valid()
        return Response(output(message="list of User Info", 
                               data=serializer.data),
                               status=status.HTTP_200_OK)

def download_csv(request, name_file):
    """
    Download a CSV file.

    Returns:
    - HTTP Response: Downloaded CSV file
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{name_file}"'
    # Write the CSV file content to the response
    return response_download_csv(response, name_file)