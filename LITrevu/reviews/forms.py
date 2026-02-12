from django import forms
from reviews.models import Ticket, Review
from django.core.validators import MinValueValidator, MaxValueValidator

class TicketForm(forms.Form):
    title = forms.CharField(required=False)
    description = forms.CharField(max_length=1000)
    image = forms.ImageField()


class ReviewForm(forms.Form):
    title = forms.CharField(required=False)
    description = forms.CharField(max_length=1000)
    image = forms.ImageField()
    rating = forms.IntegerField(validators=[
        MinValueValidator(0),  # minimum autorisé
        MaxValueValidator(5)   # maximum autorisé
    ])
    body = forms.CharField(max_length=8192)