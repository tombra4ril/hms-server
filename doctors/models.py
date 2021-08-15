from django.db import models
from account.models import Profile
from departments.models import Departments
import uuid

class Doctors(models.Model):
  uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  department = models.ForeignKey(Departments, max_length=50, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.profile.firstname} {self.profile.lastname}"

  class Meta:
    ordering = ["pk"]