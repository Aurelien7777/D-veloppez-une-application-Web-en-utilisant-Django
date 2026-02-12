from django.shortcuts import render
from .forms import TicketForm

# Create your views here.


def ticket_view(request):
    form = TicketForm()
    return render(request, "reviews/ticket.html")