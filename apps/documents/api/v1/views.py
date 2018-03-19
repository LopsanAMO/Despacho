# -*- coding: utf-8 -*-
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import HttpResponse
from django.db.models import Q
from rest_framework import status, generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from utils.helpers import LargeResultsSetPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import (
    AllUserClientSerializer, ClientSerializer, ClientFolderSerializer,
    DocumentDetailSerializer, FolderSerializer
)
from users.helpers import get_jwt_user
from users.decorators import validate_jwt
from documents.models import UserClient, Document, FolderClient
from utils.helpers import RequestInfo


class UserListAPIView(generics.ListAPIView):
    """UserListAPIView
    Args:
        :param order: (str) newer or older
        :param limit: (int) limit pagination per page, default 10
     """
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
    """ClientListAPIView
    Args:
        :param order: (str) newer or older
        :param limit: (int) limit pagination per page, default 10
    """
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


class ClientFolderListAPIView(generics.ListAPIView):
    """ClientFolderListAPIView
    Args:
        :param name: (str) the name of the client
    """
    authentication_class = (JSONWebTokenAuthentication,)
    serializer_class = ClientFolderSerializer

    def get_queryset(self):
        queryset = UserClient.objects.all()
        if self.request.query_params.get('name') is not None:
            queryset = queryset.filter(
                slug=self.request.query_params.get('name'))
        else:
            queryset = queryset
        return queryset


class DocumentListAPIView(generics.ListAPIView):
    """DocumentListAPIView
    Args:
        :param folder: (str) the name of the folder
    """
    authentication_class = (JSONWebTokenAuthentication,)
    serializer_class = DocumentDetailSerializer
    queryset = Document.objects.all()

    def get_queryset(self):
        if self.request.query_params.get('folder') is not None:
            queryset = self.queryset.filter(
                folder=FolderClient.objects.get(
                    slug=self.request.query_params.get('folder')
                )
            )
        else:
            queryset = queryset
        return queryset


class UserClientDetailAPIView(APIView):
    def get_object(self, pk):
        """get_object
        Description:
            Get UserClient object or None
        Args:
            :param pk: (int) UserClient's pk
        """
        req_inf = RequestInfo()
        try:
            return UserClient.objects.get(pk=pk)
        except UserClient.DoesNotExist as e:
            return e.args[0]

    def put(self, request, pk):
        """UserClientDetailAPIView put
        Description:
            update client information
        """
        req_inf = RequestInfo()
        user_client = self.get_object(pk)
        if isinstance(user_client, UserClient):
            serializer = ClientSerializer(user_client, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return req_inf.status_200()
            return req_inf.status_400(serializer.errors)
        else:
            return req_inf.status_404(user_client)


class UserClientAPIView(APIView):
    @validate_jwt
    def post(self, request):
        """UserClientAPIView post
        Description:
            Create clients
        Args:
            :param name: (str) the name of the client
        """
        req_inf = RequestInfo()
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return req_inf.status_200()
        else:
            return req_inf.status_400(serializer.errors)


class FolderAPIView(APIView):
    def post(self, request):
        """FolderAPIView post
        Description:
            Create folders
        Args:
            :param name: (str) the name of the folder
        """
        req_inf = RequestInfo()
        serializer = FolderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return req_inf.status_200()
        else:
            return req_inf.status_400(serializer.errors)



class FolderClientAPIView(APIView):
    def get_object(self, pk):
        """get_object
        Description:
            Get FolderClient object or None
        Args:
            :param pk: (int) FolderClient's pk
        """
        req_inf = RequestInfo()
        try:
            return FolderClient.objects.get(pk=pk)
        except FolderClient.DoesNotExist as e:
            return e.args[0]

    def put(self, request, pk=None):
        """FolderClientAPIView put
        Description:
            update client information
        """
        req_inf = RequestInfo()
        folder_client = self.get_object(pk)
        if isinstance(folder_client, FolderClient):
            serializer = FolderSerializer(folder_client, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return req_inf.status_200()
            return req_inf.status_400(serializer.errors)
        else:
            return req_inf.status_404(folder_client)
