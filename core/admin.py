from django.contrib import admin
from .models import Department, Employee, Attendance, Performance

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'department', 'hire_date', 'is_active')
    list_filter = ('is_active', 'department', 'gender')
    search_fields = ('employee_id', 'user__username', 'user__first_name', 'user__last_name')
    date_hierarchy = 'hire_date'

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'check_in', 'check_out')
    list_filter = ('status', 'date')
    search_fields = ('employee__user__username', 'employee__employee_id')
    date_hierarchy = 'date'

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'review_date', 'reviewer', 'average_score')
    list_filter = ('review_date', 'reviewer')
    search_fields = ('employee__user__username', 'employee__employee_id', 'reviewer__username')
    date_hierarchy = 'review_date'

    def average_score(self, obj):
        return obj.average_score
    average_score.short_description = 'Average Score'
