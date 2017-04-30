# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from userprofiles.serializers import UserSerializer
from django.contrib.auth.models import Permission
from rest_framework.permissions import AllowAny
from provider.utils import get_token_expiry


class LoginUserApi(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        objec = get_token_expiry(public=True)
        print objec
        if username is None or username == '' or password is None or password == '':
            return Response({'message': 'Ingrese los campos obligatorios', 'status': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({'message': u'Usuario o contraseña incorrecto', 'status': 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                serializer = UserSerializer(user)
                return Response({'user': serializer.data, 'status': 200}, status=status.HTTP_200_OK)
