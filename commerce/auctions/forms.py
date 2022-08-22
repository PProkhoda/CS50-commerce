from django import forms
from django.core.exceptions import ValidationError

from .models import *


class AddListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'image_url', 'category', 'start_bid', 'description', 'creator']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}),
            'image_url': forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}),
            'description': forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 10})
        }
        exclude = ["creator"]


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['commenter', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 4})
        }
        exclude = ["commenter"]
        
        
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']
