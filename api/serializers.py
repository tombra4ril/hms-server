from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from decouple import config
from account.models import Account, Profile
from rest_framework import serializers

class LoginSerializer(TokenObtainPairSerializer):
  class Meta:
    model = Account
    fields = [
      "email",
      "password",
    ]
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    # get profile of user
    account = Account.objects.get(email=user.email)
    profile = Profile.objects.get(account=account)
    # Add custom claims
    token['category'] = profile.category
    token['email'] = user.email
    token['expires_in'] = config(
      "TOKEN_EXPIRES_IN",
      default="15"
    )
    token['expires_in_type'] = config(
      "TOKEN_EXPIRES_IN_TYPE",
      default="minutes"
    )
    # ...
    return token

  def validate(self, attrs):
    data = super().validate(attrs)
    # get the profile of the user
    account = Account.objects.get(email=self.user.email)
    profile = Profile.objects.get(account=account)
    # Add extra responses here should you wish
    data["category"] = profile.category # This is also used to validate user
    # data["email"] = self.user.email
    return data