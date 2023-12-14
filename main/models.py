from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    img = models.ImageField(upload_to="images/")


class Authors(models.Model):
    full_name = models.CharField(max_length=250)
    bio = models.TextField()
    img = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.full_name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Status(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.full_name
