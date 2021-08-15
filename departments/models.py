import uuid
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Departments(models.Model):
  # fields
  uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False) 
  name = models.CharField(unique=True, max_length=20)
  description = models.CharField(max_length=300)
  
  def __str__(self):
    return f"{self.name[0].upper()}{self.name[1:]}"

  def save(self, *args, **kwargs):
    self.name = self.name.lower()
    super().save(*args, **kwargs)

  class Meta:
    ordering = ["name"]