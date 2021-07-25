"""api_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# Add swagger documentation
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

#for version 1
version = "v1"

schema_view = get_schema_view(
   openapi.Info(
      title="Hospital Management API",
      default_version='v1',
      description="Api description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="tombra4ril@gmail.com"),
      license=openapi.License(name="TombraIncorp License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
#    path(r'doc', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path(f'api/{version}/docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
urlpatterns += [
    path('admin', admin.site.urls),
    path(f"api/{version}/category", include("category.urls")),
    path(f"api/{version}/auth", include("api.urls")),
    path(f"api/{version}/departments", include("departments.urls"))
]