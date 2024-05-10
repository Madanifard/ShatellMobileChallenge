from rest_framework import serializers
from user.models import AdminUser, UserInfo
from .lib import is_email_valid, is_valid_iran_code
from user.lib import create_bulk_user_info

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = AdminUser
        fields = ['email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = AdminUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserInfoSerializer(serializers.Serializer):

    email = serializers.EmailField()
    national_id = serializers.CharField(max_length=200)

    def validate_email(self, value):
        if not is_email_valid(value):
            raise serializers.ValidationError("Invalid email format")
        return value

    def validate_national_id(self, value):
        if not is_valid_iran_code(value):
            raise serializers.ValidationError("Invalid National ID")
