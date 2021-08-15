from doctors.models import Doctors
# rest framework
from drf_spectacular.utils import (
  extend_schema,
  OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework.response import Response
from rest_framework.permissions import (
  IsAuthenticated,
)
from rest_framework.decorators import (
  api_view, 
  permission_classes,
)

@api_view(http_method_names=["GET",])
@permission_classes([IsAuthenticated,])
@extend_schema(
  request=None,
  responses={
    200: OpenApiTypes.OBJECT,
    400: OpenApiTypes.OBJECT,
    401: OpenApiTypes.OBJECT,
  },
  examples=[
    OpenApiExample(
      "Success",
      description="Completed successfully",
      response_only=True,
      status_codes=["200"],
    ),
    OpenApiExample(
      "Failure",
      description="Failed. Authorization header was not set",
      response_only=True,
      status_codes=["401"],
    ),
    OpenApiExample(
      "Failure",
      description="Something went wrong",
      response_only=True,
      status_codes=["500"],
    ),
  ]
)
def doctor_patient_nurse_count(request):
  try:
    doctors = Doctors.objects.all().count()
    patients = 0
    nurses = 0
    data = {
      "doctors": doctors,
      "patients": patients,
      "nurses": nurses,
    }
    return Response(data, status=200)
  except Exception as error:
    print(f"Error: {error}")
    return Response({
        "error": "Something went wrong"
      },
      status = 500
    )