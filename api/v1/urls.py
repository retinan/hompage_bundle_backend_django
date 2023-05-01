from django.urls import path, include
from rest_framework import routers
from .views import *
from dj_rest_auth.registration.urls import urlpatterns as registration_urls
from api.views import CustomRegisterView, CustomLoginView

router = routers.DefaultRouter()

router.register('board', BoardViewSet, basename='board')
# router.register('board/<int:board_pk>/comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('board/<int:pk>/comment', comment_create, name='comment_create'),
    path('board/<int:board_pk>/comment/<int:comment_pk>/delete', comment_delete, name='comment_delete'),
    # 회원가입, 로그인 커스텀
    # 순서가 중요 커스텀 url을 기본 제공 url 보다 먼저 위치해야 함.
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/signup/', CustomRegisterView.as_view(), name='signup'),
    # dj_rest_auth 회원가입, 로그인 기본 제공 URL
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
]
