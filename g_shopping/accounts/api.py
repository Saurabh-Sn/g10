from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import Http404

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .serializers import (RegisterUserSerializer, ListUserSerializer, LoginSerializer)


class RegistrationView( mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serialized = RegisterUserSerializer(data=request.data, context={'request': request})
        if serialized.is_valid(raise_exception=True):
            users = serialized.create()
            serialized = ListUserSerializer(users)
            return Response(serialized.data, status=201)
        raise Http404


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)