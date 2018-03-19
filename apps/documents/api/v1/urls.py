from django.urls import path, include
from .views import (
    UserListAPIView, ClientListAPIView, ClientFolderListAPIView,
    DocumentListAPIView, UserClientAPIView, UserClientDetailAPIView
)

urlpatterns = [
    path('all', UserListAPIView.as_view(), name='all_clients'),
    path('clients', UserClientAPIView.as_view(), name='clients'),
    path(
        'clients/<int:pk>/',
        UserClientDetailAPIView.as_view(),
        name='clients_detail'
    ),
    path('clients/all', ClientListAPIView.as_view(), name='client_list'),
    path('folders/all', ClientFolderListAPIView.as_view(), name='folder_list'),
    path('documents', DocumentListAPIView.as_view(), name='documents_list')
]
