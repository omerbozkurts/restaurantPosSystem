from django.db import models

class Coffee(models.Model):
    name_of_coffee = models.CharField(max_length=200)
    price = models.IntegerField()
 

