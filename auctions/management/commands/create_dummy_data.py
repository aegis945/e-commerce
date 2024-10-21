import requests
from django.core.management.base import BaseCommand
from auctions.models import AuctionListing, Category
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create dummy data for Auction Listings'

    def handle(self, *args, **kwargs):
        response = requests.get('https://fakestoreapi.com/products?limit=10')
        products = response.json()

        categories = {product['category'] for product in products}
        for category in categories:
            Category.objects.get_or_create(category_name=category)

        User = get_user_model() 
        owner = User.objects.get(username='artiom.lek')

        for product in products:
            category = Category.objects.get(category_name=product['category'])
            AuctionListing.objects.create(
                item_name=product['title'],
                description=product['description'],
                category=category,
                image_url=product['image'],
                starting_bid=product['price'],
                current_bid=product['price'],
                owner=owner, 
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 10 dummy products!'))
