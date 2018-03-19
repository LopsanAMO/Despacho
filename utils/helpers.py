import re
import jwt
import json
from django.shortcuts import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from users.models import User


class RequestInfo(object):
    def __init__(self, message=None, status=status.HTTP_400_BAD_REQUEST):
        self.empty = empty_list = ['', ' ', None]
        self.data = {
            'status': status,
            'detail': message
        }

    def status_404(self, message='Informacion no encontrada'):
        self.data['status'] = status.HTTP_404_NOT_FOUND
        self.data['detail'] = message
        return self.return_status(self.data)

    def status_405(self, message='Metodp HTTP no permitido'):
        self.data['status'] = status.HTTP_405_METHOD_NOT_ALLOWED
        self.data['detail'] = message
        return self.return_data(self.data)

    def status_400(self, message='solicitud incorrecta'):
        self.data['status'] = status.HTTP_400_BAD_REQUEST
        self.data['detail'] = message
        return self.return_status(self.data)

    def status_402(self, message='Tipo de pago requerido'):
        self.data['status'] = status.HTTP_402_PAYMENT_REQUIRED
        self.data['detail'] = message
        return self.return_status(self.data)

    def status_401(self, message='Login requerido'):
        self.data['status'] = status.HTTP_401_UNAUTHORIZED
        self.data['detail'] = message
        return self.return_status(self.data)

    def status_200(self, message='Ok'):
        self.data['status'] = status.HTTP_200_OK
        self.data['detail'] = message
        return self.return_status(self.data)

    def return_status(self, data):
        return HttpResponse(
            json.dumps(data),
            content_type='application/json',
            status=data['status']
        )


class ErrorMesages(object):
    var_required = ''
    var_invalid = ''

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email)
            raise serializers.ValidationError('Email ya registrado')
        except ObjectDoesNotExist:
            return email
        except Exception as e:
            raise serializers.ValidationError(e)
        return email


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 20
