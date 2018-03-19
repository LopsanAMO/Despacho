# -*- coding: utf-8 -*-
import jwt
import json
from functools import wraps
from django.conf import settings
from django.shortcuts import HttpResponse
from rest_framework import status


def get_jwt_token(request):
    try:
        token = request.stream.META.get('HTTP_AUTHORIZATION', None)
    except AttributeError:
        token = request.request.stream.META.get('HTTP_AUTHORIZATION', None)
    return token


def validate_jwt(view_func):
    @wraps(view_func)
    def new_view_func(request, *args, **kwargs):
        token = get_jwt_token(request)
        if token is not None:
            try:
                user_jwt = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=['HS256']
                )
                return view_func(request, *args, **kwargs)
            except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:  # NOQA
                data = {
                    'status': status.HTTP_403_FORBIDDEN,
                    'detail': 'Token invalido'
                }
            except Exception as e:
                data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'detail': "{}".format(e.args[0])
                }
            return HttpResponse(
                json.dumps(data),
                content_type='application/json',
                status=data['status']
            )
        else:
            return HttpResponse(
                {
                    'Error': "Internal server error"
                },
                status="500"
            )
    return new_view_func
