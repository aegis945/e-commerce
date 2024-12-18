from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal

# inherits from django's abstract user
class User(AbstractUser):
    watchlist = models.ManyToManyField('AuctionListing', blank=True, related_name="watchlisted_by")


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.category_name
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['category_name']


class AuctionListing(models.Model):
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="won_listings")
    creation_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    def __str__(self) -> str:
        return self.item_name
    
    class Meta:
        ordering = ['item_name']


class Bid(models.Model):
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="bids")
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"User {self.user} has made a bid of {self.bid_amount} on the item {self.auction_listing} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class Comment(models.Model):
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="comments")
    comment_text = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Comment by {self.user} on '{self.auction_listing}' at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
