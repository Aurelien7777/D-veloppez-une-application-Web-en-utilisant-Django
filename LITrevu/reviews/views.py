from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm, ReviewForm, UserFollows, FollowForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

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




@login_required
def follows_view(request):
    """
    Page "Abonnements" :
    - GET  : affiche la liste des utilisateurs suivis + un formulaire pour en suivre un nouveau
    - POST : traite le formulaire (ajout d'un abonnement)
    """

    # 1) Liste des abonnements actuels de l'utilisateur connecté
    following_relations = UserFollows.objects.filter(user=request.user).select_related("followed_user")

    # 2) Formulaire par défaut (vide)
    form = FollowForm()

    # 3) Message d'erreur (si besoin)
    error = None

    if request.method == "POST":
        form = FollowForm(request.POST)

        if form.is_valid():
            username_to_follow = form.cleaned_data["username"].strip()

            # A) Empêcher "se suivre soi-même"
            if username_to_follow == request.user.username:
                error = "Vous ne pouvez pas vous suivre vous-même."
            else:
                # B) Vérifier que l'utilisateur existe
                try:
                    user_to_follow = User.objects.get(username=username_to_follow)
                except User.DoesNotExist:
                    error = "Cet utilisateur n'existe pas."
                else:
                    # C) Vérifier si déjà suivi (sinon unique_together peut faire planter)
                    already_following = UserFollows.objects.filter(
                        user=request.user,
                        followed_user=user_to_follow,
                    ).exists()

                    if already_following:
                        error = "Vous suivez déjà cet utilisateur."
                    else:
                        # D) Créer l'abonnement
                        UserFollows.objects.create(
                            user=request.user,
                            followed_user=user_to_follow,
                        )
                        return redirect("follows")  # recharger la page

    context = {
        "form": form,
        "following_relations": following_relations,
        "error": error,
    }
    return render(request, "reviews/follows.html", context)

@login_required
def unfollow_user_view(request, pk):
    """
    Désabonnement :
    - On supprime une relation UserFollows
    - IMPORTANT : suppression uniquement via POST
    - Sécurité : on vérifie que l'objet appartient bien à request.user
    """

    # 1) Si quelqu'un tente de désabonner via GET -> on refuse (bonne pratique)
    if request.method != "POST":
        return redirect("follows")

    # 2) On récupère la relation ou 404 si elle n'existe pas
    follow_relation = get_object_or_404(UserFollows, pk=pk)

    # 3) Sécurité : seul le user qui a créé la relation peut la supprimer
    if follow_relation.user != request.user:
        return redirect("follows")

    # 4) Suppression de la relation en base
    follow_relation.delete()

    # 5) Retour vers la page des abonnements
    return redirect("follows")
    