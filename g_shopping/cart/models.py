from django.db import models
from accounts.models import User
from  product.models import  Product
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='user_cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
