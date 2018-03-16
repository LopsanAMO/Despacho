import jwt
import json
from django.contrib.auth.middleware import get_user
from django.conf import settings
from django.shortcuts import HttpResponse
from rest_framework import serializers
from rest_framework import status
from users.models import User


def verify_data(data, field):
    empty_list = ['', ' ', None]
    if data not in empty_list and data != field:
        return True
    else:
        return Falses


def get_jwt_user(request):
    user_jwt = get_user(request)
    try:
        if user_jwt.is_authenticated():
            return user_jwt
    except Exception:
        pass
    token = request.META.get('HTTP_AUTHORIZATION', None)
    user_jwt = None
    if token is not None:
        try:
            user_jwt = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            user_jwt = User.objects.get(
                id=user_jwt['user_id']
            )
        except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:  # NOQA
            raise serializers.ValidationError('Token invalido')
        except Exception as e:
            user_jwt = None
    return user_jwt


def get_jwt_user_header(request):
    user_jwt = get_user(request)
    if user_jwt.is_authenticated():
        return user_jwt
    token = request.GET.get('HTTP_AUTHORIZATION', None)
    user_jwt = None
    if token is not None:
        try:
            user_jwt = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            user_jwt = User.objects.get(
                id=user_jwt['user_id']
            )
        except Exception as e:
            user_jwt = None
    return user_jwt
