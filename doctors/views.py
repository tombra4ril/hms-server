from core.common import get_category_name_from_initials
from django.shortcuts import render
from django.db import (
  transaction,
  IntegrityError,
)
from .models import Doctors
from account.models import (
  Account,
  Profile,
)
from departments.models import Departments
from core.common import get_category_initials
from rest_framework import fields
from rest_framework.decorators import (
  api_view, 
  permission_classes
)
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (
  DoctorSerializer,
  AddDoctorSerializer,
)
from .models import Doctors
from django.contrib.auth import get_user_model
from drf_spectacular.utils import (
  extend_schema,
  inline_serializer,
  # OpenApiParameter, 
  OpenApiExample
)
from drf_spectacular.types import OpenApiTypes

# get the user model
Account = get_user_model()

# Create your views here.
@permission_classes((IsAuthenticated,))
@extend_schema( 
  responses={
    200: OpenApiTypes.OBJECT,
    500: OpenApiTypes.OBJECT,
  },
  examples=[
    OpenApiExample(
      "Success",
      description="Completed successfully",
      value={
        "doctors": [{
          "firstname": "string", 
          "lastname": "string",
          "department": "string",
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
      status_codes=["500"],
    ),
  ]
)
@api_view(http_method_names=["GET"])
def list_doctors(request):
  """List all the doctors in the doctors table"""
  try:
    data = Doctors.objects.all()
    serializer = DoctorSerializer(data, many=True)
    return Response({"doctors": serializer.data}, status=200)
  except Exception as error:
    print(f"Error: {error}")
    return Response({
        "details": "error",
        "error": str(error)
      },
      status=500
    )

@permission_classes((IsAuthenticated,))
@extend_schema( 
  responses={
    200: OpenApiTypes.OBJECT,
    500: OpenApiTypes.OBJECT,
  },
  examples=[
    OpenApiExample(
      "Success",
      description="Completed successfully",
      value={
        "doctors": [{
          "firstname": "string", 
          "lastname": "string",
          "department": "string",
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
      status_codes=["500"],
    ),
  ]
)
@api_view(http_method_names=["GET"])
def list_doctor(request, uuid):
  """List all the doctors in the doctors table"""
  try:
    data = Doctors.objects.get(uuid=uuid)
    serializer = DoctorSerializer(data)
    return Response({"doctor": serializer.data}, status=200)
  except Exception as error:
    return Response({
        "details": "error",
        "error": str(error)
      },
      status=500
    )

@permission_classes((IsAuthenticated,))
@extend_schema( 
  request=inline_serializer(
    name = "Add doctor",
    fields = {
      "email": serializers.CharField(),
      "password": serializers.CharField(),
      "firstname": serializers.CharField(),
      "lastname": serializers.CharField(),
      "address": serializers.CharField(),
      "phone": serializers.CharField(),
      "department": serializers.CharField(),
    }
  ),
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
@transaction.atomic
def add_doctors(request):
  """
  Adds a doctor to the doctors table
  """
  try:
    with transaction.atomic():
      email = request.data["email"]
      password = request.data["password"]
      department = request.data["department"]
      if email != "" or password != "" or department != "":
        # create a new account
        account = Account(
          email=email,
          password=password,
        )
        account.save()

        # create a new profile
        category = get_category_name_from_initials("doctor")
        profile = Profile(
          account=account,
          category=category,
          firstname=request.data["firstname"],
          lastname=request.data["lastname"],
          address=request.data["address"],
          phone=request.data["phone"],
        )
        profile.save()

        # get the department instance
        department_instance = Departments.objects.filter(name = department.lower()).first()
        # create a new doctor
        doctor = Doctors(
          profile=profile,
          department=department_instance,
        )
        doctor.save()

        return Response({"details": "ok"}, status=200)
      return Response({"details": "supply all details"}, status=400)
  except IntegrityError as error:
    print(f"Error: ", error)
    return Response({"details": "error", "error": str(error)}, status=400)

@permission_classes((IsAuthenticated,))
@extend_schema( 
  request=inline_serializer(
    name = "Add doctor",
    fields = {
      "firstname": serializers.CharField(),
      "lastname": serializers.CharField(),
      "department": serializers.CharField(),
    }
  ),
  responses={
    200: OpenApiTypes.OBJECT,
    400: OpenApiTypes.OBJECT,
    500: OpenApiTypes.OBJECT,
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
      description="Details not corrected sent to server",
      value={"details": "One or more data not properly formated or is empty"},
      response_only=True,
      status_codes=["400"],
    ),
    OpenApiExample(
      "Failure",
      description="Error, Internal error",
      value={"details": "error", "error": "string"},
      response_only=True,
      status_codes=["500"],
    )
  ]
)
@api_view(http_method_names=["PUT"])
def edit_doctor(request, uuid):
  """
  Adds a doctor to the doctors table
  """
  try:
    firstname = request.data["firstname"]
    lastname = request.data["lastname"]
    department = request.data["department"].lower()
    if firstname != "" or lastname != "" or department != "":
      doctor = Doctors.objects.get(uuid = uuid)
      data = {
        "profile": {
          "firstname": firstname,
          "lastname": lastname,
        },
        "department": {
          "name": department
        }
      }
      serializer = DoctorSerializer(instance=doctor, data=data)
      if serializer.is_valid():
        serializer.save()
        return Response({"details": "ok"}, status=200)
      print(f"Error: {serializer.errors}")
      return Response({"details": "supply all details"}, status=400)
  except Exception as error:
    print(f"Exception error: {error}")
    return Response({"details": "error", "error": str(error)}, status=500)
