from django.urls import path, include
from .views import *


app_name = 'accounts'

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('', include('django.contrib.auth.urls')),
]
