from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("cat", views.cat, name="cat"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("comments/<int:id>", views.comments, name="comments"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bids/<int:id>", views.bids, name="bids"),
    path("closeListing/<int:id>", views.closeListing, name="closeListing"),

]
