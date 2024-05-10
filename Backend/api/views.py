from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializer import LoginSerializer, RegistrationSerializer, UserInfoSerializer
from django.http import HttpResponse
from django.urls import reverse
from .lib import (read_csv_file, 
                  create_csv_file, 
                  output, 
                  convert_error_to_str, 
                  response_download_csv, 
                  insert_user_info, 
                  list_user_info)


class LoginAPIView(APIView):
    def post(self, request):
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
    def post(self, request):
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
    
    def post(self, request):
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

    def get(self, request):
        user_info_list = list_user_info()
        print('@'*40)
        print(user_info_list)
        print('@'*40)
        serializer = UserInfoSerializer(data=user_info_list, many=True)
        serializer.is_valid()
        return Response(output(message="list of User Info", 
                               data=serializer.data),
                               status=status.HTTP_200_OK)

def download_csv(request, name_file):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{name_file}"'
    # Write the CSV file content to the response
    return response_download_csv(response, name_file)