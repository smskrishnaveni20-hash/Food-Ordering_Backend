from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Restaurants(models.Model):
    Images = models.ImageField(upload_to="media",null=True, blank = True)
    Restaurant_Name = models.CharField(max_length=35)
    Restaurant_Location = models.TextField(max_length=250)
    Mobile_Number = PhoneNumberField(max_length=13, default="000 000 0000")
    Url_Offical = models.URLField(max_length=200, blank= True, null= True)
    Rating = models.DecimalField(max_digits=5, decimal_places=1)

    def __str__(self):
        return self.Restaurant_Name

