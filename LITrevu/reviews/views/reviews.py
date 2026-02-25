"""
Vues liées aux critiques (Review).

Ce fichier regroupe :
- création d'une critique (cas simple)
- création d'une critique en réponse à un ticket
- modification d'une critique
- suppression d'une critique
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import ReviewForm
from ..models import Review, Ticket


@login_required
def create_review_view(request):
    """
    Crée une critique "simple".

    Attention :
    - Dans ton projet, la critique est normalement liée à un Ticket.
    - Cette vue sert si tu as une page "Créer une critique" indépendante.
    - Si ton formulaire ReviewForm n'inclut pas le champ ticket,
      cette vue ne pourra pas fonctionner (car Review.ticket est obligatoire).
    """

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            # commit=False permet de compléter les champs obligatoires
            review = form.save(commit=False)

            # On force l'auteur à être l'utilisateur connecté
            review.user = request.user

            # Si Review.ticket est obligatoire et que ton form ne le demande pas,
            # alors review.ticket sera manquant => erreur au save().
            # Dans ton cas, tu utilises surtout :
            # - create_ticket_and_review_view (ticket + review)
            # - create_review_response_view (review en réponse à un ticket)
            review.save()

            return redirect("feed")

    else:
        form = ReviewForm()

    return render(request, "reviews/review.html", {"form": form})


@login_required
def create_review_response_view(request, ticket_id):
    """
    Crée une critique (Review) en réponse à un ticket existant.

    Règles :
    - On récupère le ticket via son id.
    - On empêche l'utilisateur de poster 2 reviews sur le même ticket.
    - GET  : affiche le formulaire vide + le ticket.
    - POST : enregistre la review liée au ticket.
    """

    # Récupérer le ticket ou 404 s'il n'existe pas
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Empêcher la double critique sur le même ticket par le même user
    already_reviewed = Review.objects.filter(user=request.user, ticket=ticket).exists()
    if already_reviewed:
        return redirect("feed")

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            # commit=False : on complète user + ticket avant sauvegarde
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect("feed")
    else:
        form = ReviewForm()

    context = {
        "form": form,
        "ticket": ticket,
    }
    return render(request, "reviews/review_response.html", context)


@login_required
def update_review_view(request, review_id):
    """
    Modifie une critique existante.

    Règles :
    - Seul l'auteur peut modifier.
    - GET  : formulaire pré-rempli.
    - POST : sauvegarde.
    """

    review = get_object_or_404(Review, id=review_id)

    # Sécurité : seul l'auteur peut modifier
    if review.user != request.user:
        return redirect("feed")

    if request.method == "POST":
        # instance=review => mise à jour de l'objet existant
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            return redirect("feed")
    else:
        form = ReviewForm(instance=review)

    context = {
        "form": form,
        "review": review,
    }
    return render(request, "reviews/review_edit.html", context)


@login_required
def delete_review_view(request, review_id):
    """
    Supprime une critique.

    Règles :
    - Suppression uniquement via POST.
    - Seul l'auteur peut supprimer.
    """

    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return redirect("feed")

    if request.method != "POST":
        return redirect("feed")

    review.delete()
    return redirect("feed")