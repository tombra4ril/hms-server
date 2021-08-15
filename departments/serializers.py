from .models import Departments
from django.core import serializers
from rest_framework.response import Response
from rest_framework import serializers as Serializers
import json
from departments.models import Departments

class DepartmentNames(Serializers.ModelSerializer):
  class Meta:
    model = Departments
    fields = ["name"]

def list_departments_serializer():
  records = Departments.objects.all()
  serialized_records = serializers.serialize("json", records, fields=("uuid", "name", "description")) # returns a string
  filtered_data = json.loads(serialized_records) # converts to python list (in json format is accurate)
  # convert the data to a list to send back
  filtered_data = [_["fields"] for _ in filtered_data]
  return filtered_data # returns the fields dictionary

def list_department_serializer(uuid):
  try:
    dept = Departments.objects.get(uuid = uuid)
    data = {
      "uuid": dept.uuid,
      "name": dept.name,
      "description": dept.description,
    }
    return data
  except Exception as error:
    print(f"Error is: {error}")
    
class AddDepartmentSerializer(Serializers.ModelSerializer):
  class Meta:
    model = Departments
    fields = ["name", "description"]
  