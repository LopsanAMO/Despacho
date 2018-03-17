from django.urls import path, include
from .views import UserListAPIView, ClientListAPIView

urlpatterns = [
    path('all', UserListAPIView.as_view(), name='all_clients'),
    path('clients', ClientListAPIView.as_view(), name='clients_list')
]
