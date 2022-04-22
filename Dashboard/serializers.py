from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken




class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['first_name', 'last_name', 'school', 'grade', 'student_number']

    def get_first_name(self,obj):
        first_name = obj.first_name
        return first_name

class StudentSerializerWithToken(StudentSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Students
        fields = ['first_name', 'last_name', 'school', 'grade', 'student_number', 'token']

    def get_token(self,obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)