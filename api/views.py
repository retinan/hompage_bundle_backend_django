
from rest_framework import status
from rest_framework.response import Response
from dj_rest_auth.registration.views import RegisterView
from api.serializers.accountSerializer import CustomLoginSerializer, CustomRegisterSerializer
from dj_rest_auth.views import LoginView


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    # def create(self, request, *args, **kwargs):
    #
    #     # 약관 동의 체크 여부 확인
    #     if not request.data.get('isCheck'):
    #         return Response({'non_field_errors': '약관에 동의해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
    #     return super().create(request, *args, **kwargs)


