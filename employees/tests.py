from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Employee


class EmployeeTests(APITestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_user(username="admin", password="adminpass")
        self.client.login(username="admin", password="adminpass")
        # Login and get the JWT token
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'admin', 'password': 'adminpass'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_employee(self):
      url = reverse('employee-list-create')
      data = {
          "name": "John Doe",
          "email": "john.doe@example.com",
          "department": "Engineering",
          "role": "Developer"
      }
      response = self.client.post(url, data, format='json')
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertEqual(Employee.objects.count(), 1)
      self.assertEqual(Employee.objects.get().name, "John Doe")
    
    def test_list_employees(self):
      # Create multiple employees for pagination
      for i in range(15):
          Employee.objects.create(
              name=f"Employee {i}",
              email=f"employee{i}@example.com",
              department="Engineering",
              role="Developer"
          )
      url = reverse('employee-list-create') + '?page=1'
      response = self.client.get(url, format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(len(response.data), 10)  # Should return only 10 due to pagination

    def test_retrieve_employee(self):
      employee = Employee.objects.create(
          name="Jane Doe",
          email="jane.doe@example.com",
          department="HR",
          role="Manager"
      )
      url = reverse('employee-detail', args=[employee.id])
      response = self.client.get(url, format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data['name'], employee.name)

    def test_update_employee(self):
      employee = Employee.objects.create(
          name="John Doe",
          email="john.doe@example.com",
          department="Engineering",
          role="Developer"
      )
      url = reverse('employee-detail', args=[employee.id])
      data = {
          "name": "John Doe Updated",
          "role": "Senior Developer"
      }
      response = self.client.put(url, data, format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      employee.refresh_from_db()
      self.assertEqual(employee.name, "John Doe Updated")
      self.assertEqual(employee.role, "Senior Developer")
    
    def test_delete_employee(self):
      employee = Employee.objects.create(
          name="John Doe",
          email="john.doe@example.com",
          department="Engineering",
          role="Developer"
      )
      url = reverse('employee-detail', args=[employee.id])
      response = self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
      self.assertEqual(Employee.objects.count(), 0)





