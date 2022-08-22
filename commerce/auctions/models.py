# from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Categories(models.Model):
    category = models.CharField(max_length=32)
    
    def __str__(self):
        return self.category


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    image_url = models.URLField(max_length=300, default="https://as2.ftcdn.net/v2/jpg/04/87/28/07/1000_F_487280776_70nVPeKBJquslGgmpLrWQuEJ34QKahzR.jpg")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    start_bid = models.IntegerField(default=0)
    current_bid = models.FloatField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="creators_listings")
    watched_by = models.ManyToManyField(User, blank=True, related_name="whatched_listings")
    buyer = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.title


class Bid(models.Model):
    Listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingbids")
    date_bid = models.DateTimeField(default=timezone.now)
    bider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userBids")
    bid = models.FloatField()

    def __str__(self):
        return f"{self.bider}: {self.bid}"


class Comments(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingCommets")
    date = models.DateTimeField(default=timezone.now)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userCommets")
    comment = models.TextField(max_length=300)
    
    def __str__(self):
        return f"{self.commenter}: {self.comment}"
    