# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from userprofiles.serializers import UserSerializer
from django.contrib.auth.models import Permission
from rest_framework.permissions import AllowAny


class LoginUserApi(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username is None or username == '' or password is None or password == '':
            return Response({'message': 'Ingrese los campos obligatorios'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({'message': 'El usuario no existe'}, status=status.HTTP_200_OK)
            else:
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
