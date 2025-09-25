from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_student', 'is_teacher', 'is_admin', 'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined', 'is_active']


