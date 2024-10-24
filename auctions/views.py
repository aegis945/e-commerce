from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .forms import AuctionListingForm, CommentForm
from .models import AuctionListing, Bid, Category, Comment, User
from decimal import Decimal


def index(request):
    listings = AuctionListing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("auctions:index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect("auctions:index")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("auctions:index")
    else:
        return render(request, "auctions/register.html")
    
@login_required
def watchlist(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def toggle_watchlist(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)

    if listing in request.user.watchlist.all():
        request.user.watchlist.remove(listing)
    else:
        request.user.watchlist.add(listing)

    return redirect("auctions:listing_page", listing_id=listing_id)

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listings(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = AuctionListing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })

@login_required(login_url="auctions:login")
def create_listing(request):
    if request.method == "POST":
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.current_bid = listing.starting_bid
            listing.save()
            return redirect("auctions:index")
    else:
        form = AuctionListingForm()

    return render(request, "auctions/create_listing.html", {
        "form": form
    })

def listing_page(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    bids = listing.bids.all()
    comments = listing.comments.all()
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)  # Bind the form with request data
        if form.is_valid():
            comment = form.save(commit=False)
            comment.auction_listing = listing
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect("auctions:listing_page", listing_id=listing_id)
        
    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "comments": comments,
        "form": form,
        "bids": bids
    })

@login_required(login_url="auctions:login")
def bid_on_listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    message = ""

    if request.method == "POST":
        bid_amount = request.POST.get("bid_amount")

        if listing.is_active:
            if Decimal(bid_amount) >= listing.starting_bid and listing.current_bid is None or Decimal(bid_amount) > listing.current_bid:
                Bid.objects.create(auction_listing=listing, user=request.user, bid_amount=bid_amount)

                listing.current_bid = bid_amount
                listing.winner = request.user
                listing.save()
            
                messages.success(request, "You have successfully placed your bid!")
                return redirect("auctions:listing_page", listing_id=listing_id)
            else:
                message = f"Bid must be greater than the current highest bid {listing.current_bid}"
        else:
            message = "This auction has already closed."

    return render(request, "auctions/listing_page.html", {
        "listing": listing, 
        "message": message
    })

@login_required(login_url="auctions:login")
def close_auction(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    
    if request.user == listing.owner and listing.is_active:
        listing.is_active = False
        listing.save()

    return redirect("auctions:listing_page", listing_id=listing_id)

@login_required
def won_listings(request):
    listings = AuctionListing.objects.filter(winner=request.user, is_active=False)
    return render(request, "auctions/won_listings.html", {
        "listings": listings
    })