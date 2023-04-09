from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.IntegerField()
    photo = models.URLField()
    closed = models.BooleanField(default=False)
    category = models.CharField(max_length=64)
    sold_price = models.IntegerField(default=0)

    def __str__(self):
        return "Listing: " + f"{self.title}"

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    price = models.IntegerField()

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    comment = models.TextField()

class Watchlists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)
