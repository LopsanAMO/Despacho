# -*- coding: utf-8 -*-
import json
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from .serializers import (
    AllUserClientSerializer, ClientSerializer, ClientFolderSerializer,
    DocumentDetailSerializer, FolderSerializer, DocumentInfoSerializer,
    ClientSimpleSerializer, FolderSimpleSerializer
)
from documents.models import UserClient, Document, FolderClient
from utils.helpers import RequestInfo, LargeResultsSetPagination


@api_view(['GET'])
def user_by_name(request):
    from django.shortcuts import HttpResponse
    from django.template import defaultfilters
    name = defaultfilters.slugify(request.GET.get('name'))
    try:
        serializer = ClientSerializer(
            UserClient.objects.filter(slug__icontains=name).order_by('name'),
            many=True)
        return HttpResponse(
            json.dumps({
                "results": serializer.data,
                "count": len(serializer.data)}),
            content_type='application/json',
            status=200
        )
    except Exception:
        return HttpResponse(
            json.dumps({"results": [], "count": 0}),
            content_type='application/json',
            status=200
        )


@api_view(['GET'])
def document_by_name(request):
    from django.shortcuts import HttpResponse
    from django.template import defaultfilters
    name = defaultfilters.slugify(request.GET.get('name'))
    try:
        serializer = DocumentDetailSerializer(
            Document.objects.filter(slug__icontains=name).order_by('name'),
            many=True
        )
        return HttpResponse(
            json.dumps({
                "results": serializer.data,
                "count": len(serializer.data)
            }),
            content_type='application/json',
            status=200
        )
    except Exception:
        return HttpResponse(
            json.dumps({"results": [], "count": 0}),
            content_type='application/json',
            status=200
        )


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
        order = None
        queryset = self.queryset
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
                try:
                    serializer.save()
                    return req_inf.status_200()
                except Exception as e:
                    return req_inf.status_400(e.args[0])
            return req_inf.status_400(serializer.errors)
        else:
            return req_inf.status_404(user_client)

    permission_classes = (IsAdminUser, )

    def delete(self, request, pk=None):
        """UserClientDetailAPIView delete
        Description:
            delete clients
        Args:
            :param name: (str) client name
        """
        req_inf = RequestInfo()
        name = request.query_params.get('name', None)
        if name is not None:
            try:
                client = UserClient.objects.get(slug=name)
                folders = FolderClient.objects.filter(user=client)
                for folder in folders:
                    documents = Document.objects.filter(folder=folder)
                    for doc in documents:
                        doc.document.delete()
                        doc.delete()
                client.delete()
                return req_inf.status_200()
            except Exception as e:
                return req_inf.status_400(e.args[0])
        else:
            return req_inf.status_400('Nombre de cliente requerido')


class UserClientAPIView(APIView):
    def get(self, request):
        """UserClientAPIView get
        Description:
            Get client id
        Args:
            :param name: (str) client slug name
        """
        req_inf = RequestInfo()
        name = request.GET.get('name', None)
        try:
            serializer = ClientSimpleSerializer(
                UserClient.objects.get(slug=name))
            return Response(serializer.data)
        except Exception as e:
            return req_inf.status_400(e.args[0])

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
            try:
                serializer.save()
                return req_inf.status_200()
            except Exception as e:
                return req_inf.status(e.args[0])
        else:
            return req_inf.status_400(serializer.errors)


class FolderAPIView(APIView):
    def get(self, request):
        """FolderAPIView get
        Description:
            Get folder id
        Args:
            :param name: (str) folder slug name
        """
        req_inf = RequestInfo()
        name = request.GET.get('name', None)
        if name is not None:
            try:
                serializer = FolderSimpleSerializer(
                    FolderClient.objects.get(slug=name))
                return Response(serializer.data)
            except Exception as e:
                return req_inf.status_400(e.args[0])
        else:
            return req_inf.status_400('nombre de folder requerido')

    def post(self, request):
        """FolderAPIView post
        Description:
            Create folders
        Args:
            :param name: (str) the name of the folder
            :param user: (int) user id
        """
        req_inf = RequestInfo()
        serializer = FolderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return req_inf.status_200()
            except Exception as e:
                return req_inf.status_400(e.args[0])
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

    permission_classes = (IsAdminUser, )

    def delete(self, request, pk=None):
        """FolderClientAPIView delete
        Description:
            delete folder
        Args:
            :param name: (str) folder name
        """
        req_inf = RequestInfo()
        name = request.query_params.get('name', None)
        if name is not None:
            try:
                folder = FolderClient.objects.get(slug=name)
                documents = Document.objects.filter(folder=folder)
                for doc in documents:
                    doc.document.delete()
                    doc.delete()
                folder.delete()
                return req_inf.status_200()
            except Exception as e:
                return req_inf.status_400(e.args[0])
        else:
            return req_inf.status_400('Nombre de folder requerido')


class DocumentAPIView(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        """DocumentAPIView post
        Description:
            Create Documents
        Args:
            :param name: (str) the name of the document
            :param document: (file) document file
            :param folder: (id) folder id
        """
        req_inf = RequestInfo()
        serializer = DocumentInfoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return req_inf.status_200()
            except Exception as e:
                return req_inf.status_400(e.args[0])
        else:
            return req_inf.status_400(serializer.errors)


class DocumentDetailAPIView(APIView):
    def get_object(self, pk):
        """get_object
        Description:
            Get Document object or None
        Args:
            :param pk: (int) Document's pk
        """
        req_inf = RequestInfo()
        try:
            return Document.objects.get(pk=pk)
        except Document.DoesNotExist as e:
            return e.args[0]

    def put(self, request, pk):
        """DocumentDetailAPIView put
        Description:
            update document information
        """
        req_inf = RequestInfo()
        document_cls = self.get_object(pk)
        if isinstance(document_cls, Document):
            serializer = DocumentInfoSerializer(
                document_cls,
                data=request.data
            )
            if serializer.is_valid():
                try:
                    serializer.save()
                    return req_inf.status_200()
                except Exception as e:
                    return req_inf.status_400(e.args[0])
            return req_inf.status_400(serializer.errors)
        else:
            return req_inf.status_404(document_cls)

    permission_classes = (IsAdminUser, )

    def delete(self, request, pk=None):
        """DocumentDetailAPIView delete
        Description:
            Delete Documents
        Args:
            :param name: (str) the name of the document
        """
        req_inf = RequestInfo()
        name = request.query_params.get('name', None)
        if name is not None:
            try:
                document = Document.objects.get(slug=name)
                document.document.delete()
                document.delete()
                return req_inf.status_200()
            except Exception as e:
                return req_inf.status_400(e.args[0])
        else:
            return req_inf.status_400('Nombre de documento requerido')
