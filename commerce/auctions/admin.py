from django.contrib import admin
from .models import Listing, Bid, Comments, Categories

# Register your models here.
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(Categories)
