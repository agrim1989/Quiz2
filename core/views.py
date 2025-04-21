from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, F
from django.utils import timezone
from datetime import timedelta
from .models import Department, Employee, Attendance, Performance
from .serializers import (
    DepartmentSerializer, EmployeeSerializer,
    AttendanceSerializer, PerformanceSerializer
)

# Create your views here.

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def employee_count(self, request, pk=None):
        department = self.get_object()
        count = department.employees.count()
        return Response({'employee_count': count})

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def attendance_summary(self, request, pk=None):
        employee = self.get_object()
        last_month = timezone.now() - timedelta(days=30)
        
        attendance = Attendance.objects.filter(
            employee=employee,
            date__gte=last_month
        ).aggregate(
            total_days=Count('id'),
            present_days=Count('id', filter=models.Q(status='present')),
            absent_days=Count('id', filter=models.Q(status='absent'))
        )
        
        return Response(attendance)

    @action(detail=True, methods=['get'])
    def performance_summary(self, request, pk=None):
        employee = self.get_object()
        performances = Performance.objects.filter(employee=employee)
        
        summary = performances.aggregate(
            average_productivity=Avg('productivity_score'),
            average_quality=Avg('quality_score'),
            average_attendance=Avg('attendance_score'),
            average_teamwork=Avg('teamwork_score'),
            overall_average=Avg(
                (F('productivity_score') + 
                 F('quality_score') + 
                 F('attendance_score') + 
                 F('teamwork_score')) / 4
            )
        )
        
        return Response(summary)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def department_summary(self, request):
        last_month = timezone.now() - timedelta(days=30)
        
        summary = Attendance.objects.filter(
            date__gte=last_month
        ).values(
            'employee__department__name'
        ).annotate(
            total_attendance=Count('id'),
            present_count=Count('id', filter=models.Q(status='present')),
            absent_count=Count('id', filter=models.Q(status='absent')),
            late_count=Count('id', filter=models.Q(status='late'))
        )
        
        return Response(summary)

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def department_analytics(self, request):
        analytics = Performance.objects.values(
            'employee__department__name'
        ).annotate(
            avg_productivity=Avg('productivity_score'),
            avg_quality=Avg('quality_score'),
            avg_attendance=Avg('attendance_score'),
            avg_teamwork=Avg('teamwork_score'),
            overall_avg=Avg(
                (F('productivity_score') + 
                 F('quality_score') + 
                 F('attendance_score') + 
                 F('teamwork_score')) / 4
            )
        )
        
        return Response(analytics)
