from . import views as api_view
from django.urls import path

urlpatterns = [
  path("", api_view.CategoryListView.as_view(), name="category_category_list_view")
]
