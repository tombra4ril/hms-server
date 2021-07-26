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
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
from drf_spectacular.utils import (
  extend_schema,
  inline_serializer,
  # OpenApiParameter, 
  OpenApiExample
)
from drf_spectacular.types import OpenApiTypes

# Create your views here.
@extend_schema( 
  responses=AddDepartmentSerializer,
)
@permission_classes((IsAuthenticated,))
@api_view(http_method_names=["GET"])
def list_departments(request):
  """List all the departments in the departments table"""
  data = list_departments_serializer()
  # print(f"type is: {type(data)} and data is {data}")
  return Response({"departments": data})

# name_param = openapi.Parameter(
#   'name', 
#   openapi.IN_QUERY, 
#   description="Name of department", 
#   type=openapi.TYPE_STRING,
#   required=True
# )
# desc_param = openapi.Parameter(
#   'description', 
#   openapi.IN_QUERY, 
#   description="Description of the department", 
#   type=openapi.TYPE_STRING,
#   required=True
# )
@permission_classes((IsAuthenticated,))
@extend_schema( 
  parameters=[
    AddDepartmentSerializer,  # serializer fields are converted to parameters
  ], 
  request=AddDepartmentSerializer,
  responses={
    200: OpenApiTypes.OBJECT,
    400: OpenApiTypes.OBJECT,
  },
  examples=[
    OpenApiExample(
      "Success",
      description="Completed successfully",
      value={"detail": "success"},
      response_only=True,
      status_codes=["200"],
    ),
    OpenApiExample(
      "Failure",
      description="Error, failed",
      value={"detail": "error"},
      response_only=True,
      status_codes=["400"],
    )
  ]
)
@api_view(http_method_names=["POST"])
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
  