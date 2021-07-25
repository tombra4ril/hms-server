from .models import Category
from .serializers import CategorySerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# Create your views here.

class CategoryListView(APIView):
  permission_classes = [AllowAny]
  def get(self, request):
    categories = Category.objects.all()
    serializer = CategorySerializers(categories, many=True)
    return Response(serializer.data)