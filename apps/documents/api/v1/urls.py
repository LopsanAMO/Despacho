from django.urls import path, include
from .views import (
    UserListAPIView, ClientListAPIView, ClientFolderListAPIView,
    DocumentListAPIView
)

urlpatterns = [
    path('all', UserListAPIView.as_view(), name='all_clients'),
    path('clients/all', ClientListAPIView.as_view(), name='client_list'),
    path('folders/all', ClientFolderListAPIView.as_view(), name='folder_list'),
    path('documents', DocumentListAPIView.as_view(), name='documents_list')
]
