from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

def index(request):
    return render(request, "auctions/index.html", {
    "listings": Listings.objects.filter(closed=False), "owner": request.user
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createlisting(request):
    if request.method == "POST":
        user = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        photo = request.POST["url"]
        category = request.POST["category"]
        listing = Listings(user=user, title=title, description=description, price=price, photo=photo, category=category)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        categories = ["Fashion", "Kitchen", "Furniture", "Electronics", "Food", "Entertainment"]
        return render(request, "auctions/createlisting.html", {
            "categories": categories
        })

def listing(request, id):
    listing = Listings.objects.get(id=id)
    user = request.user

    if request.method == "POST":
        comment = request.POST["comment"]
        comment = Comments(user=user, listing=listing, comment=comment)
        comment.save()
    bid_price = last_bid(listing)
    
    try:
        watchlists = Watchlists.objects.filter(user=user)
        cond = False
        for watchlist in watchlists:
            if watchlist.listing == listing:
                cond = True
        return render(request, "auctions/listing.html", {
                    "listing": listing, "owner": user,
                    "comments": Comments.objects.filter(listing=listing), "cond": cond, "signedin": True, "bid_price": bid_price
                })
    except:
        return render(request, "auctions/listing.html", {
                    "listing": listing, "owner": user,
                    "comments": Comments.objects.filter(listing=listing), "signedin": False, "bid_price": bid_price
                })

def addwatchlist(request, id):
    listing = Listings.objects.get(id=id)
    user = request.user
    try: 
        x = Watchlists.objects.get(user=user, listing=listing)
        return render(request, "auctions/error.html", {
            "cond": False
        }) 
    except:
        watchlist = Watchlists(user=user, listing=listing)
        watchlist.save()
        return HttpResponseRedirect(reverse("listing", kwargs={'id': id}))
    
def removewatchlist(request, id):
    listing = Listings.objects.get(id=id)
    watchlist = Watchlists.objects.get(user=request.user, listing=listing)
    watchlist.delete()
    return HttpResponseRedirect(reverse("listing", kwargs={'id': id}))

def submitbid(request, id):
    pbid = int(request.GET["bid"])
    listing = Listings.objects.get(id=id)
    bid_price = last_bid(listing)

    if pbid > bid_price:
        bid_price = pbid
        bid = Bids(user=request.user, listing=listing, price=bid_price)
        bid.save()  
        return HttpResponseRedirect(reverse("listing", kwargs={'id': id}))
    else:
        return render(request, "auctions/error.html", {
            "cond": True
        })

def closeauction(request, id):
    listing = Listings.objects.get(id=id)
    watchlists = Watchlists.objects.filter(listing=listing)   
    bid = Bids.objects.filter(listing=listing).last()   

    for watchlist in watchlists:
        watchlist.closed = True
        watchlist.save()
    listing.closed = True
    listing.user = bid.user
    listing.sold_price = bid.price
    listing.save()
    return HttpResponseRedirect(reverse("index"))

def watchlist(request): 
    watchlists = Watchlists.objects.filter(user=request.user, closed=False)
    listings = []
    for watchlist in watchlists:
        listings.append(watchlist.listing)
    return render(request, "auctions/index.html", {
    "listings": listings, "owner": request.user
    })

def wonauctions(request):
    user = request.user
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.filter(closed=True, user=user), "owner": user
    })

def categories(request):
    if request.method == "POST":
        category = request.POST["category"]
        listings = Listings.objects.filter(category=category, closed=False)
        return render(request, "auctions/index.html", {
            "listings": listings, "owner": request.user
            })
    categories = ["Fashion", "Kitchen", "Furniture", "Electronics", "Food", "Entertainment"]
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def last_bid(listing):
    bid = Bids.objects.filter(listing=listing).last()
    if bid is None:
        bid_price = listing.price
    else:
        bid_price = bid.price
    return bid_price