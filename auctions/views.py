from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .forms import AuctionListingForm
from .models import AuctionListing, User


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
    pass

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
    return render(request, "auctions/listing_page.html",{
        "listing": listing,
    })
