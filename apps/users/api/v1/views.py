# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import CreateUserSerializer, UserSerializer
from users.models import User
from users.handlers import generate_jwt
from utils.helpers import RequestInfo


class UserAPIView(APIView):

    def get(self, request):
        """Get user data
        :param Authorization: token
        :return UserSerializer: json user data
        """
        request_info = RequestInfo()
        if request.user is not None:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            raise AuthenticationFailed()

    permission_classes = (AllowAny, )

    def post(self, request):
        """Creates user accounts
        :param email: str
        :param first_name: str
        :param last_name: str
        :param password: str
        :return token: jwt_token
        """
        import re
        try:
            if request.data['username'] in [None, '', ' ']:
                request.data['username'] = re.sub(
                    "[!@#$%^&*()[]{};:,./<>?\|`~-=_+]",
                    " ",
                    request.data['email'][:(request.data['email'].find('@'))]
                )
        except Exception:
            pass
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'token': generate_jwt(serializer.instance)
            })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request):
        """Update user account data
        :param email: str
        :param first_name: str
        :param last_name: str
        :param username: str
        :param password: str
        :param phone: str
        :param genre: str
        :param birthdate: date
        :param profile_photo: file
        :return token: jwt_token
        """
        user = request.user
        request_info = RequestInfo()
        serializer = UserSerializer(user, data=request.data)
        if user is not None and serializer.is_valid():
            serializer.save()
            return request_info.return_status({
                'status': status.HTTP_200_OK,
                'token': generate_jwt(user),
                'detail': 'user updated'
            })
        else:
            raise AuthenticationFailed()
