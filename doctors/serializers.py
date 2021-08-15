from rest_framework import serializers
from .models import Doctors
from account.models import Profile
from departments.models import Departments
from django.contrib.auth.validators import UnicodeUsernameValidator

class DepartmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Departments
    fields = [
      "name",  
    ]
    extra_kwargs = {
      'name': {
        'validators': [UnicodeUsernameValidator()],
      }
    }

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = [
      "firstname", 
      "lastname",  
    ]

class DoctorSerializer(serializers.ModelSerializer):
  profile = ProfileSerializer()
  department = DepartmentSerializer()
  class Meta:
    model = Doctors
    # fields = "__all__"
    fields = [
      "uuid",
      "profile",  
      "department",
    ]
  def update(self, instance, validated_data):
    try:
      # profile serializing
      if validated_data.get("profile"):
        profile_data = validated_data.get("profile")
        profile_serializer = ProfileSerializer(data=profile_data)
        if profile_serializer.is_valid():
          profile = profile_serializer.update(
            instance=instance.profile,
            validated_data=profile_serializer.validated_data
          )
          validated_data["profile"] = profile
      if validated_data.get("department"):
        department_data = validated_data.get("department")
        department_instance = Departments.objects.get(name=department_data["name"])
        department_serializer = DepartmentSerializer(data=department_data)
        if department_serializer.is_valid():
          department = department_serializer.update(
            instance=department_instance,
            validated_data=department_serializer.validated_data,
          )
          validated_data["department"] = department
      # return instance
      return super().update(instance, validated_data)
    except Exception as error:
      print(f"Serializer error: {error}")
      return 

class AddDoctorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Doctors
    fields = "__all__"