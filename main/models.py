from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    img = models.ImageField(upload_to="images/")
    count = models.BooleanField(default=True)


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
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)

    def __str__(self):
        return self.author.full_name


class StatusUser(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)




    def __str__(self):
        return self.text

