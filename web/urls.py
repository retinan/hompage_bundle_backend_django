from django.urls import path, include


urlpatterns = [
    path('board/', include('web.board.urls')),
    path('accounts/', include('web.accounts.urls')),
]
