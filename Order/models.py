from django.db import models
from django.contrib.auth.models import User
from Dishes.models import Dishes

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user}"

class Payment(models.Model):
   PAYMENT_METHOD_CHOICES = (
       ('GPAY', 'Google Pay'),
       ('PHONEPE', 'PhonePe'),
       ('PAYTM', 'Paytm'),
       ('CARD', 'Debit / Credit Card'),
       ('COD', 'Cash On Delivery'),
   )
   PAYMENT_STATUS_CHOICES = (
       ('Pending', 'Pending'),
       ('Success', 'Success'),
       ('Failed', 'Failed'),
   )

   order = models.OneToOneField(Order, on_delete=models.CASCADE)
   payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
   payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       return f"Payment for Order {self.order.id}" 

    