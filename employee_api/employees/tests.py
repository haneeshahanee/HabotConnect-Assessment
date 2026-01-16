from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Employee


class EmployeeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.employee_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'department': 'Engineering',
            'role': 'Developer'
        }

    def test_create_employee(self):
        response = self.client.post('/api/employees/', self.employee_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().name, 'John Doe')

    def test_create_employee_duplicate_email(self):
        self.client.post('/api/employees/', self.employee_data)
        response = self.client.post('/api/employees/', self.employee_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_employee_empty_name(self):
        data = self.employee_data.copy()
        data['name'] = ''
        response = self.client.post('/api/employees/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_employees(self):
        Employee.objects.create(**self.employee_data)
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_employee(self):
        employee = Employee.objects.create(**self.employee_data)
        response = self.client.get(f'/api/employees/{employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')

    def test_retrieve_nonexistent_employee(self):
        response = self.client.get('/api/employees/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_employee(self):
        employee = Employee.objects.create(**self.employee_data)
        update_data = {
            'name': 'Jane Doe',
            'email': 'john@example.com',
            'department': 'HR',
            'role': 'Manager'
        }
        response = self.client.put(f'/api/employees/{employee.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        employee.refresh_from_db()
        self.assertEqual(employee.name, 'Jane Doe')
        self.assertEqual(employee.department, 'HR')

    def test_delete_employee(self):
        employee = Employee.objects.create(**self.employee_data)
        response = self.client.delete(f'/api/employees/{employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)

    def test_filter_by_department(self):
        Employee.objects.create(**self.employee_data)
        Employee.objects.create(
            name='Jane Smith',
            email='jane@example.com',
            department='HR',
            role='Manager'
        )
        response = self.client.get('/api/employees/?department=HR')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['department'], 'HR')

    def test_pagination(self):
        for i in range(15):
            Employee.objects.create(
                name=f'Employee {i}',
                email=f'employee{i}@example.com',
                department='Engineering',
                role='Developer'
            )
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_user_login(self):
        User.objects.create_user(username='testuser', password='testpass123')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_invalid_login(self):
        data = {
            'username': 'wronguser',
            'password': 'wrongpass'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
