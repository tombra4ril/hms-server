from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
# blacklist classes
from rest_framework_simplejwt.tokens import RefreshToken
# token obtain pair classes
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LoginSerializer
# refresh token classes
from rest_framework_simplejwt.views import TokenRefreshView
# datetime import
import datetime
# api version
version = "v1"
# get environment variables
from decouple import config
from core.common import token_time


""" 
  Create your views here.
"""

class BlacklistTokenView(APIView):
  permission_classes = [AllowAny]
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

  def post(self, request, *args, **kwargs):
    """ Check if the user can login """
    try:
      # authenticate user for category
      category = request.data.get("category")
      # instantiate the serializer with the request data
      serializer = self.serializer_class(data=request.data)
      # you must call .is_valid() before accessing validated_data
      serializer.is_valid(raise_exception=True) 
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
          response = Response({"access_token": access_token}, status=200)
          path = "/"
          response.set_cookie('refresh', refresh_token, httponly=True, expires=expiration_time, samesite="None", secure=True, path=path)
          return response
        return Response({"Error": "Something went wrong"}, status=400)
      else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
      print(f"Error => {error}")
      return Response(status=status.HTTP_403_FORBIDDEN)

class RefreshView(TokenRefreshView):
  # serializer_class = RefreshSerializer
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
        raise Exception
      return Response({"access_token": access_token}, status=200)
    except Exception as error:
      print(f"Error is: {error}")
      return Response("Error message", status=status.HTTP_403_FORBIDDEN)

class TestAuthentication(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request):
    print("User is authorized")
    return Response("Is Authenticated")