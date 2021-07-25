from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (
  AbstractBaseUser,
  BaseUserManager
)
import os
import uuid

# callable for uploading profile images
def upload_to_profile(self, filename):
  file_path = os.path.join("profile_images", self.pk, filename)
  return file_path
# callable for default profile images
def default_profile():
  file_path = os.path.join("profile_images", "default.jpg")
  return file_path

# Create your models here.
class AccountManager(BaseUserManager):
  # override functions
  def create_user(self, email, password=None):
    if not email:
      raise ValueError("Email must be specified!")
    if not password:
      raise ValueError("Password must be specified!")
    user = self.model(
      email = self.normalize_email(email)
    )
    user.set_password(password)
    user.save(using=self._db)
    return user
  def create_superuser(self, email, password=None):
    user = self.create_user(email, password=password)
    user.admin = True
    user.staff = True
    user.save(using = self._db)
    return user

class Account(AbstractBaseUser):
  uuid = models.UUIDField(verbose_name="uuid", default=uuid.uuid4, unique=True)
  email = models.EmailField(verbose_name="email", max_length=255, unique=True)
  category = models.CharField(verbose_name="Category type of the user", max_length=25, default="patient")
  date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
  last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
  profile_image = models.ImageField(verbose_name="profile image", max_length=255, upload_to=upload_to_profile, null=True, default=default_profile)
  active = models.BooleanField(default=True) # can login
  staff = models.BooleanField(default=False) # for staff
  admin = models.BooleanField(default=False) # for superuser
  #important variables that needs to be set
  objects = AccountManager()
  #
  USERNAME_FIELD = "email" #username (use email as the default login input)
  REQUIRED_FIELDS = [] # required when running commands like (python manage.py createsuperuser)
  #
  def __str__(self):
    return self.email
  def has_perm(self, perm, obj=None):
    return self.admin
  def has_module_perms(self, app_label):
    return True
  @property
  def is_staff(self):
    return self.staff
  @property
  def is_admin(self):
    return self.admin
  @property
  def is_active(self):
    return self.active