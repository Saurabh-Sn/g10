from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from .serializers import CartSerializer
from django.http import Http404


class CartView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
               mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = CartSerializer
    
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        qs = Cart.objects.filter(user=self.request.user)
        return qs

    def create(self, request, *args, **kwargs):
        serialized = CartSerializer(data=request.data, context={'request': request})
        if serialized.is_valid(raise_exception=True):
            items = serialized.create()
            serialized = CartSerializer(items)
            return Response(serialized.data, status=201)
        raise Http404
