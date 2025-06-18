from django.contrib import admin
from .models import Customer, Address, Vendor, Product, Category, Cart, ProductImage, Order, OrderItem, WishList, Review, ReviewImage, PaymentMethod
# Register your models here.
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(WishList)
admin.site.register(Review)
admin.site.register(ReviewImage)
admin.site.register(PaymentMethod)
