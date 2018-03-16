from django.urls import path, include
from users.api.v1 import urls as UserUrls
from documents.api.v1 import urls as DocumentsUrls


urlpatterns = [
    path('v1/users/', include(UserUrls)),
    path('v1/documents/', include(DocumentsUrls))
]
