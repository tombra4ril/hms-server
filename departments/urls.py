from . import views
from django.urls import path

urlpatterns = [
  path("", views.list_departments, name="List_departments"),
  path("/add", views.add_department, name="Add_department")
]