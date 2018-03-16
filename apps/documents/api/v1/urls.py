from django.urls import path, include
from .views import UserListAPIView

urlpatterns = [
    path('all', UserListAPIView.as_view(), name='clients_list'),
]
