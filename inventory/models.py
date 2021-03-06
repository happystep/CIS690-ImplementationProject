from django.db import models

# Create your models here.


class Item(models.Model):
    description = models.CharField(max_length=200)
    cost_per_item = models.IntegerField(default=0)
    item_discontinued = models.BooleanField(default=False)
    name = models.CharField(max_length=200)


class Vendor(models.Model):
    description = models.CharField(max_length=200, null=True)


class Order(models.Model):
    reorder = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)


class Location(models.Model):
    description = models.CharField(max_length=200)


class Category(models.Model):
    category = models.CharField(max_length=200)


class StockControl(models.Model):
    item_number = models.ForeignKey(Item, on_delete=models.CASCADE)
    stock_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    stock_quantity = models.IntegerField()
    stock_category = models.ForeignKey(Category, on_delete=models.CASCADE)


