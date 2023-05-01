from django.urls import path, include
from web.board.views import *


app_name = 'board'

urlpatterns = [
    path('', BoardListView.as_view(), name='list'),
    path('<int:pk>', BoardDetailView.as_view(), name='detail'),
    path('create', BoardCreateView.as_view(), name='create'),
    path('update/<int:pk>', BoardUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', BoardDeleteView.as_view(), name='delete'),

    path('<int:pk>/comment', comment_create, name='comment_create'),
    path('<int:board_pk>/comment/<int:comment_pk>/delete', comment_delete, name='comment_delete'),
]