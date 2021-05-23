
# Create your views here.
from .serializers import RegisterSerializer, UserSerializer
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser


from django.contrib.auth import get_user_model
User = get_user_model()


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        authenticated_user = request.user
        try:
            user_details = get_user_model().objects.get(id = authenticated_user.id)
            # user_profile = CustomUser.objects.select_related(User)
            records = UserSerializer(user_details, many=False)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data':records.data
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'detail': str(e)
                }

            print(str(e))
        return Response(response, status=status_code)


class GetAllResellers(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated)

    # resellers = CustomUser.objects.get(User.user_type == 'Reseller')

    serializer_class = UserSerializer