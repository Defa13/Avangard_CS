from rest_framework import serializers
from .models import Employee
from users.serializers import UserSerializer

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'user',
            'first_name',
            'last_name',
            'position',
            'department',
            'status',
            'base_salary',
            'manager',
            'hire_date',
            'fired_date',
            'created_at',
            'updated_at',
        ]
