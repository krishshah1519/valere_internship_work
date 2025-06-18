from tkinter.constants import CASCADE

from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False)
    name = models.CharField(max_length=45)
    DOB = models.DateField()
    gender_choices = (("Male", "Male"), ("Female", "Female"))
    gender = models.CharField(max_length=9,
                              choices=gender_choices,
                              default="Male")
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=54, default='default123')
    is_verified = models.BooleanField(default='False')

    def __str__(self):
        return self.name


class Address (models.Model):
    address_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.TextField(max_length=400)
    address_type = models.CharField(max_length=100)
    pincode = models.PositiveIntegerField()


class Vendor(models.Model):
    vendor_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False)


class Category(models.Model):
    category_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False)
    name = models.CharField(max_length=50)


class Product(models.Model):
    product_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False)
    Vendor_id = models.ForeignKey(
        Vendor, on_delete=models.CASCADE)
    Category = models.ForeignKey(
        Category, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    price = models.FloatField()
    details = models.TextField(max_length=500)
    rating = models.IntegerField


class Cart(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class ProductImage(models.Model):
    product_image_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_images = models.URLField()


class Order(models.Model):
    order_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order_item_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = Product(product_id).price


class WishList(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)


class Review(models.Model):
    review_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_detail = models.TextField(max_length=500)


class ReviewImage(models.Model):
    review_images_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False)
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    image_url = models.URLField()


class PaymentMethod(models.Model):
    payment_methods_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4(), editable=False)
