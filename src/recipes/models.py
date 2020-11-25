from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    cooking_time = models.CharField(max_length=100)
    image = models.CharField(max_length=255)

    def __str__(self):
        return self.title
