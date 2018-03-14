from django.urls import path, include

urlpatterns = [
    path('/all', )
    path('', UserAPIView.as_view(), name='user_list'),
    path('login/', LoginView.as_view(), name='user_login'),
]
