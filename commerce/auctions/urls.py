from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addwatchlist/<int:id>", views.addwatchlist, name="addwatchlist"),
    path("removewatchlist/<int:id>", views.removewatchlist, name="removewatchlist"),
    path("submitbid/<int:id>", views.submitbid, name="submitbid"),
    path("closeauction/<int:id>", views.closeauction, name="closeauction"),
    path("wonauctions", views.wonauctions, name="wonauctions"),
    path("categories", views.categories, name="categories")
]
