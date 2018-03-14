import jwt
import json
from django.shortcuts import HttpResponse
from rest_framework import status


class RequestInfo(object):
    def __init__(self, message=None, status=status.HTTP_400_BAD_REQUEST):
        self.not_found = 'Informacion no encontrada'
        self.unauthorization = 'Login requerido'
        self.bad_request = 'Error inesperado'
        self.payment_required = 'Tipo de pago requerido'
        self.empty = empty_list = ['', ' ', None]
        self.data = {
            'status': status,
            'detail': message
        }

    def status_404(self, message=None):
        self.data['status'] = status.HTTP_404_NOT_FOUND
        self.data['detail'] = message if message not in self.empty else self.not_found  # NOQA
        return self.return_status(self.data)

    def status_400(self, message=None):
        self.data['status'] = status.HTTP_400_BAD_REQUEST
        self.data['detail'] = message if message not in self.empty else self.bad_request  # NOQA
        return self.return_status(self.data)

    def status_402(self, message=None):
        self.data['status'] = status.HTTP_402_PAYMENT_REQUIRED
        self.data['detail'] = message if message not in self.empty else self.payment_required  # NOQA
        return self.return_status(self.data)

    def status_401(self, message=None):
        self.data['status'] = status.HTTP_401_UNAUTHORIZED
        self.data['detail'] = message if message not in self.empty else self.unauthorization  # NOQA
        return self.return_status(self.data)

    def status_200(self, message=None):
        self.data['status'] = status.HTTP_200_OK
        self.data['detail'] = message
        return self.return_status(self.data)

    def return_status(self, data):
        return HttpResponse(
            json.dumps(data),
            content_type='application/json',
            status=data['status']
        )
