from django.urls import path
from .views import (
  BlacklistTokenView,
  LoginView,
  RefreshView,
  TestAuthentication,
)

urlpatterns = [
    # path(f'{version}/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path(f'{version}/login/', LoginView.as_view(), name='login'),
    # path('/users_count', users_count, name='users_count'),
    path('/login', LoginView.as_view(), name='login'),
    path("/logout", BlacklistTokenView.as_view(), name="logout"),
    path('/refresh', RefreshView.as_view(), name='token_refresh'),
    path('/test', TestAuthentication.as_view(), name='test_auth'),
]