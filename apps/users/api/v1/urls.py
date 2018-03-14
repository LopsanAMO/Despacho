from django.urls import path, include
from rest_auth.views import LoginView, LogoutView
from .views import UserAPIView

urlpatterns = [
    path('', UserAPIView.as_view()),
    path('login/', LoginView.as_view()),
]
