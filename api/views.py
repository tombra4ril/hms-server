from rest_framework import status
from rest_framework.permissions import (
  AllowAny, 
  IsAuthenticated,
)
from rest_framework.decorators import (
  api_view, 
  permission_classes,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
# blacklist classes
from rest_framework_simplejwt.tokens import RefreshToken
# token obtain pair classes
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LoginSerializer
# refresh token classes
from rest_framework_simplejwt.views import TokenRefreshView
# drf_spectacular documentation
from drf_spectacular.utils import (
  extend_schema,
  OpenApiExample,
  inline_serializer
)
from drf_spectacular.types import OpenApiTypes
# datetime import
import datetime
# api version
version = "v1"
# get environment variables
from decouple import config
from core.common import token_time
# apps

""" 
  Create your views here.
"""

class BlacklistTokenView(APIView):
  permission_classes = [AllowAny]
  @extend_schema(
    request=None,
    responses={
      200: OpenApiTypes.OBJECT,
      401: OpenApiTypes.OBJECT,
    },
    examples=[
      OpenApiExample(
        "Success",
        description="Completed successfully",
        response_only=True,
        status_codes=["200"],
      ),
      OpenApiExample(
        "Failure",
        description="Failed. Authorization header was not set",
        response_only=True,
        status_codes=["401"],
      ),
    ]
  )
  def post(self, request):
    try:
      refresh_token = request.data["refresh_token"]
      token = RefreshToken(refresh_token)
      token.blacklist()
      return Response()
    except Exception as error:
      return Response(status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
  serializer_class = LoginSerializer
  @extend_schema(
    request=inline_serializer(
      name = "Login",
      fields = {
        "category": serializers.CharField(),
        "email": serializers.CharField(),
        "password": serializers.CharField(),
      }
    ),
    responses={
      200: OpenApiTypes.OBJECT,
      403: OpenApiTypes.OBJECT,
      500: OpenApiTypes.OBJECT,
    },
    examples=[
      OpenApiExample(
        "Success",
        description="Completed successfully",
        value={
          "access_token": "string",
        },
        response_only=True,
        status_codes=["200"],
      ),
      OpenApiExample(
        "Failure",
        description="Unauthorized, wrong email, password or category",
        value={
          "details": "error",
          "error": "wrong email, password or category"
        },
        response_only=True,
        status_codes=["403"],
      ),
      OpenApiExample(
        "Fatal Error",
        description="Something went wrong while processing the request!",
        value={
          "details": "error",
          "error": "something went wrong, try again"
        },
        response_only=True,
        status_codes=["500"],
      ),
    ]
  )
  def post(self, request, *args, **kwargs):
    """ Check if the user can login """
    try:
      # authenticate user for category
      category = request.data.get("category")
      # instantiate the serializer with the request data
      serializer = self.serializer_class(data=request.data)
      # you must call .is_valid() before accessing validated_data
      if serializer.is_valid(raise_exception=True):
        # get access and refresh tokens to do what you like with
        refresh_token = serializer.validated_data.get("refresh", None)
        access_token = serializer.validated_data.get("access", None)
        cat = serializer.validated_data.get("category", None)
        if(cat == category):
          # build my response and setting cookie
          if refresh_token is not None and access_token is not None:
            # response = super().post(request, *args, **kwargs)
            expiration_time = token_time(
              config(
                "REFRESH_EXPIRES_IN",
                default="hours"
              ),
              type=config(
                "REFRESH_EXPIRES_IN_TYPE",
                default="REFRESH"
              ),
              add=3
            )
            response = Response({
                "access_token": access_token
              },
              status=200
            )
            path = "/"
            response.set_cookie('refresh', refresh_token, httponly=True, expires=expiration_time, samesite="None", secure=True, path=path)
            return response
          return Response({
              "details": "error",
              "error": "wrong email, password or category"
            }, 
            status=403
          )
        else:
          return Response({
              "details": "error",
              "error": "wrong email, password or category"
            }, 
            status=403
          )
      else:
        return Response({
            "details": "no user",
            "error": "no user found"
          },
          status, 403
        )
    except Exception as error:
      print(f"Error => {error}")
      return Response({
          "details": "fatal",
          "error": "Something went wrong!"
        },
        status=500
      )

class RefreshView(TokenRefreshView):
  # serializer_class = RefreshSerializer
  @extend_schema( 
    request=None,
    responses={
      200: OpenApiTypes.OBJECT,
      400: OpenApiTypes.OBJECT,
      403: OpenApiTypes.OBJECT,
    },
    examples=[
      OpenApiExample(
        "Success",
        description="Completed successfully",
        value={
          "access_token": "string"
        },
        response_only=True,
        status_codes=["200"],
      ),
      OpenApiExample(
        "Unauthorized",
        description="No access token provided in the cookie",
        value={
          "details": "error",
          "error": "No access token",
        },
        response_only=True,
        status_codes=["400"],
      ),
      OpenApiExample(
        "Failure",
        description="Error, failed",
        value={
          "details": "error",
          "error": "failed",
        },
        response_only=True,
        status_codes=["403"],
      ),
    ]
  )
  def post(self, request, *args, **kwargs):
    try:
      cookie = {"refresh": request.COOKIES["refresh"]}
      # instantiate the serializer with the request data
      serializer = self.serializer_class(data=cookie)
      # you must call .is_valid() before accessing validated_data
      serializer.is_valid(raise_exception=True) 
      # get access token and email of client
      access_token = serializer.validated_data.get("access", None)
      email = serializer.validated_data.get("email", None)
      # add some claims
      if access_token is None or access_token == "":
        return Response({
            "details": "error",
            "error": "No access token"
          }, 
          status=400
        )
      return Response({"access_token": access_token}, status=200)
    except Exception as error:
      print(f"Error is: {error}")
      return Response({
          "details": "error",
          "error": "failed"
        }, 
        status=status.HTTP_403_FORBIDDEN
      )

class TestAuthentication(APIView):
  permission_classes = [IsAuthenticated]
  @extend_schema(
    request=None,
    responses={
      200: OpenApiTypes.OBJECT,
      401: OpenApiTypes.OBJECT,
    },
    examples=[
      OpenApiExample(
        "Success",
        description="Completed successfully",
        response_only=True,
        status_codes=["200"],
      ),
      OpenApiExample(
        "Success",
        description="Failed. Authorization header was not set",
        response_only=True,
        status_codes=["401"],
      ),
    ]
  )
  def post(self, request):
    print("User is authorized")
    return Response("Is Authenticated")