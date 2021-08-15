from django.shortcuts import render
from .models import Departments
from rest_framework import fields
from rest_framework.decorators import (
  api_view, 
  permission_classes
)
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Departments
from .serializers import (
  DepartmentNames,
  list_departments_serializer,
  list_department_serializer,
  AddDepartmentSerializer,
)
from .models import Departments
from drf_spectacular.utils import (
  extend_schema,
  inline_serializer,
  # OpenApiParameter, 
  OpenApiExample
)
from drf_spectacular.types import OpenApiTypes

# Create your views here.
@permission_classes((IsAuthenticated,))
@extend_schema( 
  responses={
    200: OpenApiTypes.OBJECT,
    400: OpenApiTypes.OBJECT,
  },
  examples=[
    OpenApiExample(
      "Success",
      description="Completed successfully",
      value={
        "departments": [{
          "uuid": "string",
          "name": "string", 
          "description": "string"
        }]
      },
      response_only=True,
      status_codes=["200"],
    ),
    OpenApiExample(
      "Failure",
      description="Error, failed",
      value={
        "details": "error",
        "error": "string"
      },
      response_only=True,
      status_codes=["400"],
    ),
  ]
)
@api_view(http_method_names=["GET"])
def list_departments(request):
  """Return all the departments in the departments table"""
  try:
    data = list_departments_serializer()
    # print(f"type is: {type(data)} and data is {data}"v )
    return Response({"departments": data})
  except Exception as error:
    return Response({
        "details": "error",
        "error": str(error)
      },
      status=400
    )

@permission_classes((IsAuthenticated,))
@extend_schema( 
  responses={
    200: OpenApiTypes.OBJECT,
    400: OpenApiTypes.OBJECT,
  },
  examples=[
    OpenApiExample(
      "Success",
      description="Completed successfully",
      value={
        "departments": [
          "string",
        ]
      },
      response_only=True,
      status_codes=["200"],
    ),
    OpenApiExample(
      "Failure",
      description="Error, failed",
      value={
        "details": "error",
        "error": "string"
      },
      response_only=True,
      status_codes=["400"],
    ),
  ]
)
@api_view(http_method_names=["GET"])
def list_department_names(request):
  """Return all the departments names"""
  try:
    names = Departments.objects.all()
    serializer = DepartmentNames(names, many=True)
    data = [_["name"] for _ in serializer.data]
    return Response({"departments": data})
  except Exception as error:
    return Response({
        "details": "error",
        "error": str(error)
      },
      status=400
    )

@permission_classes((IsAuthenticated,))
@extend_schema( 
  responses={
    200: OpenApiTypes.OBJECT,
    400: OpenApiTypes.OBJECT,
  },
  examples=[
    OpenApiExample(
      "Success",
      description="Completed successfully",
      value={
        "uuid": "uuid",
        "name": "string", 
        "description": "string"
      },
      response_only=True,
      status_codes=["200"],
    ),
    OpenApiExample(
      "Failure",
      description="Error, failed",
      value={
        "details": "error",
        "error": "string"
      },
      response_only=True,
      status_codes=["400"],
    ),
  ]
)
@api_view(http_method_names=["GET"])
def list_department(request, uuid):
  """Return a department in the departments table"""
  try:
    data = list_department_serializer(uuid)
    return Response(data, status=200)
  except Exception as error:
    return Response({
        "details": "error",
        "error": str(error)
      },
      status=400
    )

@permission_classes((IsAuthenticated,))
@extend_schema( 
  request=AddDepartmentSerializer,
  responses={
    200: OpenApiTypes.OBJECT,
    202: OpenApiTypes.OBJECT,
    400: OpenApiTypes.OBJECT,
  },
  examples=[
    OpenApiExample(
      "Success",
      description="Completed successfully",
      value={"details": "ok"},
      response_only=True,
      status_codes=["200"],
    ),
    OpenApiExample(
      "Found",
      description="Department already in database",
      value={"details": "found"},
      response_only=True,
      status_codes=["202"],
    ),
    OpenApiExample(
      "Failure",
      description="Error, failed",
      value={"details": "error", "error": "string"},
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
    data = {
      "name": request.data["name"].lower(),
      "description": request.data["description"]
    }
    # check if the department is already saved
    dept = Departments.objects.filter(name=data["name"])
    if(len(dept) < 1):
      serializer = AddDepartmentSerializer(data=data)
      if serializer.is_valid():
        serializer.save()
        print(f"Saved ({data['name']}) to database!")
        return Response({"details": "ok"})
      else:
        raise Exception
    else:
      print(f"Department ({data['name']}) already in database!")
      return Response({"details": "found"}, status=202)
  except Exception as error:
    print(f"Error: ", error)
    return Response({"details": "error", "error": str(error)}, status=400)

@permission_classes((IsAuthenticated,))
@extend_schema( 
  request=AddDepartmentSerializer,
  responses={
    200: OpenApiTypes.OBJECT,
    400: OpenApiTypes.OBJECT,
  },
  examples=[
    OpenApiExample(
      "Success",
      description="Completed successfully",
      value={"details": "ok"},
      response_only=True,
      status_codes=["200"],
    ),
    OpenApiExample(
      "Failure",
      description="Error, failed",
      value={"details": "error", "error": "string"},
      response_only=True,
      status_codes=["400"],
    )
  ]
)
@api_view(http_method_names=["PUT"])
def edit_department(request, uuid):
  """
  Adds a department to the departments table
  """
  try:
    name = request.data["name"]
    description = request.data["description"]
    if name == "" or description == "":
      return Response({"details": "please send all values"}, status=404)
    else:
      department = Departments.objects.get(uuid = uuid)
      department.name = name
      department.description = description
      department.save()
      return Response({"details": "ok"}, status=200)
  except Exception as error:
    print(f"Error: ", error)
    return Response({"details": "error", "error": str(error)}, status=400)

@permission_classes((IsAuthenticated,))
@extend_schema( 
  request=AddDepartmentSerializer,
  responses={
    204: OpenApiTypes.OBJECT,
    404: OpenApiTypes.OBJECT,
  },
  examples=[
    OpenApiExample(
      "Success",
      description="Completed successfully",
      value={"details": "ok"},
      response_only=True,
      status_codes=["204"],
    ),
    OpenApiExample(
      "Failure",
      description="Error, failed",
      value={"details": "error", "error": "Department does not exist"},
      response_only=True,
      status_codes=["404"],
    )
  ]
)
@api_view(http_method_names=["DELETE"])
def delete_department(request, uuid):
  """
  Adds a department to the departments table
  """
  try:
    print(f"deleting data with uuid: {uuid}")
    department = Departments.objects.get(uuid=uuid)
  except Exception as error:
    print(f"Error: ", error)
    return Response({"details": "error", "error": "Department does not exist"}, status=404)
  department.delete()
  return Response({"details": "ok"}, status=204)