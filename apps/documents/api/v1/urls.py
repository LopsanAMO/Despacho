from django.urls import path, include
from .views import (
    UserListAPIView, ClientListAPIView, ClientFolderListAPIView,
    DocumentListAPIView, UserClientAPIView, UserClientDetailAPIView,
    FolderClientAPIView, FolderAPIView, DocumentAPIView, DocumentDetailAPIView
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
    path('folders/', FolderAPIView.as_view(), name='folders'),
    path(
        'folders/<int:pk>',
        FolderClientAPIView.as_view(),
        name='folders_detail'
    ),
    path('folders/all', ClientFolderListAPIView.as_view(), name='folder_list'),
    path('documents/', DocumentAPIView.as_view(), name='documents'),
    path(
        'documents/<int:pk>',
        DocumentDetailAPIView.as_view(),
        name='documents_detail'
    ),
    path('documents/all', DocumentListAPIView.as_view(), name='documents_list'),
]
