from django.shortcuts import render, redirect
from .forms import TicketForm, ReviewForm
from django.contrib.auth.decorators import login_required


@login_required
def create_ticket_and_review_view(request):
    if request.method == "POST":
        form_ticket = TicketForm(request.POST, request.FILES, prefix="ticket")
        form_review = ReviewForm(request.POST, prefix="review")
        
        if form_review.is_valid() and form_ticket.is_valid():
            # PARTIE TICKET
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.save()

            #PARTIE REVIEW
            review = form_review.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("feed")

    else:
        form_ticket = TicketForm(prefix="ticket")
        form_review = ReviewForm(prefix="review")
    
    return render(request, "reviews/review_ticket.html", {"form_ticket" : form_ticket , 
                                                        "form_review" : form_review})  
        


@login_required
def create_ticket_view(request):

    if request.method == "POST":
        # créer une instance de notre formulaire et le remplir avec les données POST
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            # set the uploader to the user before saving the model
            ticket.user = request.user
            # now we can save
            ticket.save()
            return redirect("feed")
            
        """
        Exemple : 
        Les données POST sont : 
        <QueryDict: {'csrfmiddlewaretoken': ['OUsGBpHaOq8L6t9KiICU6a84HCTOfRdlEhzHDKg1OonioK5BbvItiiHVMzScJyv9'], 
        'titre': ['Demande d'avis sur le livre Harry Potter'], 
        'description': ['J'aimerais savoir pourquoi acheter ce livre !’]
        'image': ['photo.jpeg'], }>
        """
        
    else:
        # ceci doit être une requête GET, donc créer un formulaire vide
        form = TicketForm()
        
    return render(request, "reviews/ticket.html", {"form" : form}) 
#  {"form" : form} permet d'envoyer ce formulaire au gabarit (Notre HTML)

@login_required
def create_review_view(request):
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("feed")
        
    else:
        form = ReviewForm()

    return render(request, "reviews/review.html", {"form" : form})