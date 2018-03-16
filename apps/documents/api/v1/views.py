# -*- coding: utf-8 -*-
import json

from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from documents.models import UserClient
from .serializers import AllUserClientSerializer
from users.helpers import get_jwt_user
from utils.helpers import RequestInfo


class UserListAPIView(APIView):
    @permission_classes((AllowAny, ))
    def get(self, request):
        req_inf = RequestInfo()
        user = get_jwt_user(request)
        limit = request.GET.get('limit', 20)
        page = request.GET.get('page', 1)
        order = request.GET.get('order', 'newer')
        data = {}
        if user is not None:
            users = UserClient.objects.all()
            if order == 'newer':
                users.order_by('-created')
            else:
                users.order_by('createds')
            paginator = Paginator(users, limit)
            try:
                client_page = paginator.page(page)
            except PageNotAnInteger:
                posts_page = paginator.page(1)
            except EmptyPage:
                client_page = paginator.page(paginator.num_pages)
            data['num_pages'] = paginator.num_pages
            data['clients'] = AllUserClientSerializer(
                client_page.object_list,
                many=True
            ).data
            return HttpResponse(
                json.dumps(data),
                content_type='application/json',
                status=status.HTTP_200_OK
            )
        else:
            raise AuthenticationFailed()


# @csrf_exempt
# @api_view(['GET'])
# def UserListAPIView(request):
#     import pudb; pudb.set_trace()
#     req_inf = RequestInfo()
#     if request.method == 'GET':
#         user = get_jwt_user(request)
#         limit = request.GET.get('limit', 20)
#         page = request.GET.get('page', 1)
#         order = request.GET.get('order', 'newer')
#         if user is not None:
#             users = UserClient.objects.all()
#             if order == 'newer':
#                 users.order_by('-created')
#             else:
#                 users.order_by('createds')
#             paginator = Paginator(posts_cls, limit)
#             try:
#                 post_page = paginator.page(page)
#             except PageNotAnInteger:
#                 posts_page = paginator.page(1)
#             except EmptyPage:
#                 post_page = paginator.page(paginator.num_pages)
#             data['num_pages'] = paginator.num_pages
#             data['clients'] = AllUserClientSerializer(
#                 post_page.object_list,
#                 many=True
#             ).data
#             return HttpResponse(
#                 json.dumps(data),
#                 content_type='application/json',
#                 status=status.HTTP_200_OK
#             )
#         else:
#             return request_info.status_404('Usuario no encontrado')
#     else:
#         return req_inf.status_405()
