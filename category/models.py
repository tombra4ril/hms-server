from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=20)

  def __str__(self):
    return str(self.name).capitalize()

  class Meta:
    ordering = ["name"]