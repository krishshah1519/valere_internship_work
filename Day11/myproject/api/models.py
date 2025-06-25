from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
# Create your models here.


class Customer(AbstractUser):
    dob = models.DateField(default=date.today)
    gender_choices = (("Male", "Male"), ("Female", "Female"))
    gender = models.CharField(max_length=9,
                              choices=gender_choices,
                              default="Male")
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.username
