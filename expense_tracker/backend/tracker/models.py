from django.db import models

from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.


class User(AbstractUser):
    dob = models.DateTimeField(default=date.today)
    gender_choices = (("Male", "male"), ("Female", "female"))
    gender = models.CharField(choices=gender_choices, default="Male")
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.username


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"{self.category}"
