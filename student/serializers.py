from rest_framework import serializers
from .models import Student, Parent


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    parent = ParentSerializer()

    class Meta:
        model = Student
        fields = '__all__'


