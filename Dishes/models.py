from django.db import models
from Restaurants.models import Restaurants

# Create your models here.
class Dishes(models.Model):
    restaurants = models.ForeignKey(Restaurants, related_name= 'dishes', on_delete= models.CASCADE)
    Available_in = models.CharField(max_length=200, null= True)
    name = models.CharField(max_length=200,null=True)
    price = models.IntegerField(null=True)
    is_available = models.BooleanField(null=True)

    def __str__(self):
        return self.name