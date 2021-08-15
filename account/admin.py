from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib import admin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import Profile

User = get_user_model()

# Register your models here.
class AccountAdmin(BaseUserAdmin):
  form = UserAdminChangeForm # update view
  add_form = UserAdminCreationForm # create view

  list_display = (
    "email",
    "admin", 
  )
  search_fields = (
    "email",
  )
  readonly_fields = (
    "id",
    "date_joined",
    "last_login"
  )
  filter_horizontal = ()
  list_filter = (
    "admin", 
    "staff", 
    "active", 
  )
  fieldsets = (
    (None, {
      "fields": (
        "email",
        "password",
      )
    }),
    ("Personal info", {
      "fields": ()
    }),
    ("Permissions", {
      "fields": (
        "admin", 
        "staff", 
        "active",
      )
    }),
  )
  # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
  # overrides get_fieldsets to use this attribute when creating a user
  add_fieldsets = (
    (None, {
      "classes": ("wide",),
      "fields": (
        "email", 
        "password", 
        "password_2",
      ),
    }),
  )
  ordering = (
    "email",
  )

admin.site.register(User, AccountAdmin)
admin.site.register(Profile)