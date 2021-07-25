from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account

# Register your models here.
class AdminView(UserAdmin):
  list_display = (
    "email",
    "date_joined",
    "last_login",
    "profile_image",
    "active",
    "staff",
    "admin"  
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
  list_filter = ()
  fieldsets = ()
  ordering = (
    "email",
  )
  
admin.site.register(Account, AdminView)