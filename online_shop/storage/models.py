from django.db import models
from django.contrib.auth import get_user_model


class Item(models.Model):
    item_name = models.CharField(max_length=128)
    buyer = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    item_description = models.TextField()

    def __str__(self):
        return self.item_name