from django.db import models


class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
