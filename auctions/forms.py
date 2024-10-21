from django import forms
from .models import AuctionListing, Category

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["item_name", "description", "category", "image_url", "starting_bid"]

        widgets = {
            'item_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter the title of your item"
            }),
            'description': forms.Textarea(attrs={
                'rows': 4, 'class': 'form-control',
                'placeholder': "Enter a detailed description"
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': "Add an image URL"
            }),
            'starting_bid': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter the starting bid amount",
            }),
        }

        labels = {
            "item_name": "Title",
            "description": "Description",
            "category": "Category (optional)",
            "image_url": "Image URL (optional)",
            "starting_bid": "Starting Bid",
        }
        