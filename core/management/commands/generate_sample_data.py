from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Department, Employee, Attendance, Performance
from faker import Faker
from datetime import timedelta, datetime
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Generate sample data for the employee management system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating sample data...')

        # Create departments
        departments = [
            'Engineering',
            'Human Resources',
            'Marketing',
            'Sales',
            'Finance'
        ]

        dept_objects = []
        for dept_name in departments:
            dept = Department.objects.create(
                name=dept_name,
                description=fake.text()
            )
            dept_objects.append(dept)
            self.stdout.write(f'Created department: {dept_name}')

        # Create employees with users
        for i in range(5):
            # Create user
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}.{last_name.lower()}"
            user = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password='password123',
                first_name=first_name,
                last_name=last_name
            )

            # Create employee
            employee = Employee.objects.create(
                user=user,
                employee_id=f"EMP{str(i+1).zfill(4)}",
                department=random.choice(dept_objects),
                date_of_birth=fake.date_of_birth(minimum_age=22, maximum_age=65),
                gender=random.choice(['M', 'F', 'O']),
                phone_number=f"+1{fake.msisdn()[3:]}",  # Format: +1XXXXXXXXXX
                address=fake.address(),
                hire_date=fake.date_between(start_date='-5y', end_date='today'),
                salary=random.randint(30000, 120000),
            )
            self.stdout.write(f'Created employee: {employee}')

            # Generate attendance records for the last 30 days
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=30)
            current_date = start_date

            while current_date <= end_date:
                if current_date.weekday() < 5:  # Only workdays
                    status = random.choices(
                        ['present', 'absent', 'late'],
                        weights=[0.8, 0.1, 0.1]
                    )[0]
                    
                    base_time = datetime.combine(current_date, datetime.min.time())
                    check_in_time = base_time + timedelta(hours=random.randint(8, 10))
                    check_in = timezone.make_aware(check_in_time)
                    
                    check_out = None
                    if status != 'absent':
                        check_out_time = base_time + timedelta(hours=random.randint(16, 18))
                        check_out = timezone.make_aware(check_out_time)

                    Attendance.objects.create(
                        employee=employee,
                        date=current_date,
                        check_in=check_in,
                        check_out=check_out,
                        status=status,
                        notes=fake.text() if status != 'present' else ''
                    )

                current_date += timedelta(days=1)

            # Generate performance reviews
            for _ in range(2):
                review_date = fake.date_between(
                    start_date=employee.hire_date,
                    end_date='today'
                )
                
                Performance.objects.create(
                    employee=employee,
                    review_date=review_date,
                    reviewer=User.objects.order_by('?').first(),
                    productivity_score=random.randint(1, 5),
                    quality_score=random.randint(1, 5),
                    attendance_score=random.randint(1, 5),
                    teamwork_score=random.randint(1, 5),
                    comments=fake.text(),
                    goals=fake.text()
                )

        self.stdout.write(self.style.SUCCESS('Successfully generated sample data')) 