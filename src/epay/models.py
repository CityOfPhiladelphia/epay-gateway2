from django.db import models


class Department (models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class ProductCategory (models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Product (models.Model):
    name = models.TextField()
    slug = models.CharField(max_length=64)
    price = models.PositiveIntegerField(null=True, blank=True)
    summary = models.TextField()
    description = models.TextField()
    categories = models.ManyToManyField('ProductCategory')
    department = models.ManyToManyField('Department')

    def __str__(self):
        return self.name
