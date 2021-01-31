from rest_framework import serializers
from .models import Cart


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['product', 'quantity']

    def create(self, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(
            product=self.validated_data['product'],

            user=self.validated_data['user'],

        )
        if cart:
            cart.quantity = self.validated_data['quantity'],
            cart.upate()
        if created:
            created.quantity = self.validated_data['quantity'],
            created.upate()
        return cart
