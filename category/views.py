from .models import Category
from .serializers import CategorySerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# drf_spectacular documentation
from drf_spectacular.utils import (
  extend_schema,
  OpenApiExample
)
from drf_spectacular.types import OpenApiTypes

# Create your views here.

class CategoryListView(APIView):
  permission_classes = [AllowAny]
  @extend_schema( 
    responses={
      200: OpenApiTypes.OBJECT,
      400: OpenApiTypes.OBJECT,
    },
    examples=[
      OpenApiExample(
        "Success",
        description="Completed successfully",
        value={
          "categories": [{"id": "int", "name": "string"}]
        },
        response_only=True,
        status_codes=["200"],
      ),
      OpenApiExample(
        "Failure",
        description="Error, failed",
        value={
          "details": "error",
          "error": "string",
        },
        response_only=True,
        status_codes=["400"],
      ),
    ]
  )
  def get(self, request):
    try:
      categories = Category.objects.all()
      serializer = CategorySerializers(categories, many=True)
      return Response({"categories": serializer.data})
    except Exception as error:
      return Response({
        "details": "error",
        "error": str(error),
      }, status=400)