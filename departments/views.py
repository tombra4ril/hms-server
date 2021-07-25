from django.shortcuts import render
from rest_framework.decorators import (
  api_view, 
  permission_classes
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (
  list_departments_serializer,
  AddDepartmentSerializer,
)
from .models import Departments
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
@api_view(http_method_names=["POST"])
@permission_classes((IsAuthenticated,))
def list_departments(request):
  """List all the departments in the departments table"""
  data = list_departments_serializer()
  # print(f"type is: {type(data)} and data is {data}")
  return Response({"departments": data})

name_param = openapi.Parameter(
  'name', 
  openapi.IN_QUERY, 
  description="Name of department", 
  type=openapi.TYPE_STRING,
  required=True
)
desc_param = openapi.Parameter(
  'description', 
  openapi.IN_QUERY, 
  description="Description of the department", 
  type=openapi.TYPE_STRING,
  required=True
)
@permission_classes((IsAuthenticated,))
@api_view(http_method_names=["POST"])
@swagger_auto_schema(
  # manual_parameters=[name_param, desc_param], 
  # responses={
  #   200: "Successfully added a new department"
  # },
  request_body=AddDepartmentSerializer,
  # request_body=openapi.Schema(
  #   type=openapi.TYPE_OBJECT,
  #   properties={
  #     "name": openapi.Schema(
  #       type=openapi.TYPE_STRING,
  #       description="Name of department"
  #     )
  #   }
  # ),
  # operation_id="add_department",
)
def add_department(request):
  """
  Adds a department to the departments table
  """
  try:
    print("Data sent is: ", request.data, "\nUser is: ", request.user)
    data = {
      "name": request.data["name"],
      "description": request.data["desc"]
    }
    serializer = AddDepartmentSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:

      raise Exception
  except Exception as error:
    print(f"Error: no json data from client!\n", error)
    return Response({"error": "Failed to execute!"})
  