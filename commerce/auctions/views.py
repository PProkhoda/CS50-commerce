from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

# create class for "new page" Listing
# class NewEntryForm(forms.Form):
#     # title = forms.CharField(label='title', widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}))
#     # img = forms.URLField(widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}))
#     # category = forms.ChoiceField()
#     # text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 10}))
#     class Meta:
#         model = Listing
#         fields = ['title', 'image_url', 'category', 'start_bid', 'description']
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}),
#             'image_url': forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}),
#         }

def index(request):
    posts = Listing.objects.filter(status=True)
    categories = Categories.objects.all()
    currentuser = request.user
    if request.user.is_authenticated == True:
        watchlist = currentuser.whatched_listings.all().count()
        context = {
            'posts': posts,
            'categories': categories,
            'title': 'Auction',
            'watchlist': watchlist,
        }
        return render(request, "auctions/index.html", context=context)
    else:
        context = {
            'posts': posts,
            'categories': categories,
            'title': 'Auction',
        }
        return render(request, "auctions/index.html", context=context)


def cat(request):
    if request.method == "POST":
        categoryFromPOST = request.POST['category']
        category = Categories.objects.get(category=categoryFromPOST)
        posts = Listing.objects.filter(status=True, category=category)
        categories = Categories.objects.all()
        context = {
            'posts': posts,
            'categories': categories,
            'title': 'Auction',
        }
        return render(request, "auctions/index.html", context=context)


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


@login_required
def add(request):
    if request.method == "POST":
        form = AddListingForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.creator = request.user
            new_post.save()
            form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = AddListingForm()
    return render(request, 'auctions/add.html', {
        'form': form, 
        'title': 'New Listing',
    })


def listing(request, id):
    listingdata = Listing.objects.get(pk=id)
    listingWatchlist = request.user in listingdata.watched_by.all()
    currentuser = request.user
    # watchlist = currentuser.whatched_listings.all().count()
    try:
        biddata = Bid.objects.filter(Listing=listingdata).last().bider
        watchlist = currentuser.whatched_listings.all().count()
    # watched_by = listingdata.watched_by.all()
        return render(request, 'auctions/listing.html', {
            "listing": listingdata,
            "listingWatchlist": listingWatchlist,
            "user": currentuser,
            "commentform": CommentsForm(),
            "comments": listingdata.listingCommets.all(),
            "bids": listingdata.listingbids.all(),
            "winbid": biddata,
            "bidform": BidForm(),
            'watchlist': watchlist,
        })
    except:
        return render(request, 'auctions/listing.html', {
            "listing": listingdata,
            "listingWatchlist": listingWatchlist,
            "user": currentuser,
            "commentform": CommentsForm(),
            "comments": listingdata.listingCommets.all(),
            "bids": listingdata.listingbids.all(),
            "bidform": BidForm(),
            # 'watchlist': watchlist,
        })
    # request.user in listingdata.watched_by.all()


@login_required
def removeWatchlist(request, id):
    listingdata = Listing.objects.get(pk=id)
    currentuser = request.user
    listingdata.watched_by.remove(currentuser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


@login_required
def addWatchlist(request, id):
    listingdata = Listing.objects.get(pk=id)
    currentuser = request.user
    listingdata.watched_by.add(currentuser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


@login_required
def watchlist(request):
    currentuser = request.user
    listings = currentuser.whatched_listings.all()
    return render(request, 'auctions/watchlist.html',{
        "watchlists": listings
    })
    


@login_required
def comments(request, id):
    listingdata = Listing.objects.get(pk=id)
    commentform = CommentsForm(request.POST)
    newcomment = commentform.save(commit=False)
    newcomment.commenter = request.user
    newcomment.listing = listingdata
    newcomment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))


@login_required
def bids(request, id):
    listing = Listing.objects.get(pk=id)
    offer =  float(request.POST['bid'])
    user = request.user
    if user != listing.creator:
        if offer > listing.start_bid and (listing.current_bid is None or offer > listing.current_bid):
            listing.current_bid = offer
            bidform = BidForm(request.POST)
            newbid = bidform.save(commit=False)
            newbid.bider = request.user           
            newbid.Listing = listing
            newbid.save()
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=(id, )))
        else :
            return render(request, 'auctions/listing.html', {
                "listing": listing,
                "user": user,
                "bidform": BidForm(),
                "chekbid": True,
                "commentform": CommentsForm(),
            })
    else :
        return render(request, 'auctions/listing.html', {
            "listing": listing,
            "user": user,
            "bidform": BidForm(),
            "commentform": CommentsForm(),
        })


@login_required
def closeListing(request, id):
    listing = Listing.objects.get(pk=id)
    currentuser = request.user
    if currentuser == listing.creator:
        listing.buyer = Bid.objects.filter(Listing=listing).last().bider
        listing.status = False
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(id, )))
    else :
        return render(request, 'auctions/listing.html', {
            "listing": listing,
        })