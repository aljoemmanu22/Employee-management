from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Employee
from .serializers import EmployeeSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create and List Employees
class EmployeeListCreate(APIView):
    """
    get:
    Returns a list of all employees, with optional filtering by department or role.
    Pagination of 10 employees per page.

    post:
    Creates a new employee with provided details such as name, email, department, and role.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of employees",
        responses={200: EmployeeSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('department', openapi.IN_QUERY, description="Filter by department", type=openapi.TYPE_STRING),
            openapi.Parameter('role', openapi.IN_QUERY, description="Filter by role", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Pagination page number", type=openapi.TYPE_INTEGER),
        ],
    )
    def get(self, request):
        department = request.query_params.get('department')
        role = request.query_params.get('role')
        employees = Employee.objects.all()
        if department:
            employees = employees.filter(department=department)
        if role:
            employees = employees.filter(role=role)
        # Pagination: 10 employees per page
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * 10
        end = start + 10
        serializer = EmployeeSerializer(employees[start:end], many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=EmployeeSerializer,
        operation_description="Create a new employee",
        responses={201: EmployeeSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, Update, and Delete Employee
class EmployeeDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
