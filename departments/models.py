import uuid
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Departments(models.Model):
  # fields
  id_key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False) 
  name = models.CharField(max_length=20)
  description = models.CharField(max_length=300)
  
  def __str__(self):
    return f"Departments of HMS:\n(\n  name={self.name}\n)\n(\n  desc={self.description}\n)\n"