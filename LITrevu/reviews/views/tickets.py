"""
Vues liées aux tickets.

Ce fichier regroupe :
- création de ticket
- modification de ticket
- suppression de ticket
- création "ticket + review" en une seule étape
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import TicketForm, ReviewForm
from ..models import Ticket


@login_required
def create_ticket_view(request):
    """
    Crée un ticket.

    Fonctionnement :
    - GET  : affiche un formulaire vide
    - POST : valide le formulaire puis enregistre le ticket
             en forçant le user connecté comme auteur.
    """

    if request.method == "POST":
        # request.FILES est nécessaire car Ticket contient un champ image
        form = TicketForm(request.POST, request.FILES)

        if form.is_valid():
            # commit=False : on crée l'objet sans l'enregistrer,
            # pour pouvoir renseigner ticket.user avant l'enregistrement.
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            return redirect("feed")
    else:
        form = TicketForm()

    return render(request, "reviews/ticket.html", {"form": form})


@login_required
def update_ticket_view(request, ticket_id):
    """
    Modifie un ticket existant.

    Règles :
    - Seul l'auteur du ticket peut modifier.
    - GET  : formulaire pré-rempli
    - POST : sauvegarde si valide
    """

    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Sécurité : seul l'auteur peut modifier
    if ticket.user != request.user:
        return redirect("feed")

    if request.method == "POST":
        # instance=ticket => le formulaire modifie l'objet existant
        form = TicketForm(request.POST, request.FILES, instance=ticket)

        if form.is_valid():
            form.save()
            return redirect("feed")
    else:
        form = TicketForm(instance=ticket)

    return render(request, "reviews/ticket_edit.html", {"form": form, "ticket": ticket})


@login_required
def delete_ticket_view(request, ticket_id):
    """
    Supprime un ticket.

    Règles :
    - Suppression uniquement via POST.
    - Seul l'auteur peut supprimer.
    """

    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.user != request.user:
        return redirect("feed")

    # Interdire la suppression via GET
    if request.method != "POST":
        return redirect("feed")

    ticket.delete()
    return redirect("feed")


@login_required
def create_ticket_and_review_view(request):
    """
    Crée un ticket + une review en une seule étape.

    Fonctionnement :
    - Deux formulaires sur la même page :
      * TicketForm (avec prefix="ticket")
      * ReviewForm (avec prefix="review")
    - POST : si les deux formulaires sont valides :
      1) on crée le ticket (avec user=request.user)
      2) on crée la review (avec user=request.user et ticket=ticket)
    """

    if request.method == "POST":
        # prefix : évite que les champs ticket/review aient les mêmes noms HTML
        form_ticket = TicketForm(request.POST, request.FILES, prefix="ticket")
        form_review = ReviewForm(request.POST, prefix="review")

        if form_ticket.is_valid() and form_review.is_valid():
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = form_review.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect("feed")

    else:
        form_ticket = TicketForm(prefix="ticket")
        form_review = ReviewForm(prefix="review")

    return render(
        request,
        "reviews/review_ticket.html",
        {
            "form_ticket": form_ticket,
            "form_review": form_review,
        },
    )
