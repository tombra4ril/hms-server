from rest_framework import serializers
from .models import Category

class CategorySerializers(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ["id", "name"]
    # use: "__all__"  to retrieve all the columns in the table
    # use ("id", "name") to retrieve these two columns