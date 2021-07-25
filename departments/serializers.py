from .models import Departments
from django.core import serializers
from rest_framework.response import Response
from rest_framework import serializers as Serializers
import json

def list_departments_serializer():
  records = Departments.objects.all()
  serialized_records = serializers.serialize("json", records, fields=("name", "description")) # returns a string
  filtered_data = json.loads(serialized_records) # converts to python list (in json format is accurate)
  # convert the data to a list to send back
  filtered_data = [_["fields"] for _ in filtered_data]
  return filtered_data # returns the fields dictionary

class AddDepartmentSerializer(Serializers.ModelSerializer):
  class Meta:
    model = Departments
    fields = ["name", "description"]
  