from django.db import models

# Create your models here.
class user_list(models.Model):
    Username = models.CharField(max_length=255)
    Mobile = models.CharField(max_length=255)
    Password1 = models.CharField(max_length=255)
    Password2 = models.CharField(max_length=255)
    Otp = models.CharField(max_length=255)
    is_admin = models.BooleanField()
    Verified = models.BooleanField()

class product_item_list(models.Model):
    Title = models.CharField(max_length=255)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Description = models.CharField(max_length=255)
    Category = models.CharField(max_length=255)
    Images = models.ImageField(upload_to="products_imges")
    Rate = models.CharField(max_length=255, default="0")

class add_to_cart_list(models.Model):
    Userid = models.CharField(max_length=255)
    Username = models.CharField(max_length=255)
    Product_obj = models.JSONField() # Store dict/JSON directly
    Quantity = models.IntegerField(default=1) 
    TotalPrice = models.DecimalField(max_digits=10, decimal_places=2)