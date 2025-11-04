from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from catalog.models import Product

User = get_user_model()

class Order(models.Model):
    DELIVERY_CHOICES = [
        ("delivery", "Нужна доставка"),
        ("pickup", "Самовывоз"),
    ]
    PAYMENT_CHOICES = [
        ("card", "Оплата картой"),
        ("cod", "Наличными/картой при получении"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default="delivery")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="card")
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order #{self.id} by {self.first_name}'

    @property
    def total(self):
        return sum(item.total for item in self.items.all())

    def clean(self):
        if self.delivery_method == "delivery" and not (self.address or "").strip():
            raise ValidationError({"address": "Укажите адрес доставки."})

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveIntegerField(default=1)

    @property
    def total(self):
        return self.price * self.qty
