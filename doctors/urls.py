from django.urls import (
  path,
)
from .views import (
  add_doctors,
  list_doctors,
  list_doctor,
  edit_doctor,
)

urlpatterns = [
  path("", list_doctors, name="doctors"),
  path("/<uuid:uuid>", list_doctor, name="doctor"),
  path("/add", add_doctors, name="doctors_add"),
  path("/<uuid:uuid>/edit", edit_doctor, name="doctor_edit"),
]