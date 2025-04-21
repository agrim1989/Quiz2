from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Department, Employee, Attendance, Performance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='department',
        write_only=True
    )

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class AttendanceSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        source='employee',
        write_only=True
    )

    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class PerformanceSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        source='employee',
        write_only=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='reviewer',
        write_only=True
    )
    average_score = serializers.FloatField(read_only=True)

    class Meta:
        model = Performance
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at') 