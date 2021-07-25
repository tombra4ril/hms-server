from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from decouple import config

class LoginSerializer(TokenObtainPairSerializer):
  # class Meta:
  #   fields = [
  #     "email",
  #     "password",
  #     "category"
  #   ]
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    # Add custom claims
    token['category'] = user.category
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
    # Add extra responses here should you wish
    data["category"] = self.user.category # This is also used to validate user
    # data["email"] = self.user.email
    return data

# class RefreshSerializer():
#   pass