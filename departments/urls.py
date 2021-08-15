from . import views
from django.urls import path

urlpatterns = [
  path("", views.list_departments, name="List_departments"),
  path("/names", views.list_department_names, name="List_departments_names"),
  path("/<uuid:uuid>", views.list_department, name="List_department"),
  path("/add", views.add_department, name="Add_department"),
  path("/<uuid:uuid>/edit", views.edit_department, name="Edit_department"),
  path("/<uuid:uuid>/delete", views.delete_department, name="Delete_department"),
]