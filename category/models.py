from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=20)

  def __str__(self):
    return str(self.name).capitalize()

class Users(models.Model):
  Account = get_user_model()
  # fields 

  user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
  firstname = models.CharField(max_length=20)
  lastname = models.CharField(max_length=20)
  category = models.CharField(max_length=20)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    name = self.firstname + self.lastnamedd
    return str(self.name)