
from django.urls import path
from users.views import MyObtainTokenPairView, RegisterView, UserProfileView, GetAllResellers
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('user-profile/', UserProfileView.as_view(), name='auth_profile'),
    path('resellers/', GetAllResellers.as_view(), name='resellers'),
]
