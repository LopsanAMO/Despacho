# -*- coding: utf-8 -*-
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import HttpResponse
from rest_framework import status, generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from utils.helpers import LargeResultsSetPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import AllUserClientSerializer, ClientSerializer
from users.helpers import get_jwt_user
from documents.models import UserClient
from utils.helpers import RequestInfo


class UserListAPIView(generics.ListAPIView):
    authentication_class = (JSONWebTokenAuthentication,)
    queryset = UserClient.objects.all()
    serializer_class = AllUserClientSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        order = 'newer'
        if self.request.query_params.get('order') is not None:
            order = self.request.query_params.get('order')
        if order == 'newer':
            queryset = self.queryset.order_by('-created')
        else:
            queryset = self.queryset.order_by('created')
        return queryset


class ClientListAPIView(generics.ListAPIView):
    authentication_class = (JSONWebTokenAuthentication,)
    queryset = UserClient.objects.all().order_by('name')
    serializer_class = ClientSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        order = 'newer'
        if self.request.query_params.get('order') is not None:
            order = self.request.query_params.get('order')
        if order == 'newer':
            queryset = self.queryset.order_by('-created')
        else:
            queryset = self.queryset.order_by('created')
        return queryset
