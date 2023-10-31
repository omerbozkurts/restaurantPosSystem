from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField()
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_amount = models.IntegerField()
    def __str__(self):
        return self.product_name

class Sale(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)