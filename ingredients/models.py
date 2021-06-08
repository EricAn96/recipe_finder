from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, verbose_name='')

    def __str__(self):
        return self.name

class Saved_Recipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20)
    ingredients = models.CharField(max_length=200)
    image_link = models.CharField(max_length=200)