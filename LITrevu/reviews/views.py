from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm, ReviewForm, FollowForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .services import block_user, unblock_user, is_blocked
from .models import Ticket, Review, UserFollows, UserBlock
from itertools import chain  # permet de combiner plusieurs QuerySets
from django.db.models import Q, Value, CharField

User = get_user_model()


@login_required
def feed(request):
    """
    Vue principale du flux.

    On doit combiner :
    - Tickets
    - Reviews
    Puis trier le tout par date décroissante.
    """

    # ---------------------------------------------------
    # 1) Récupérer les utilisateurs suivis
    # ---------------------------------------------------

    followed_users = UserFollows.objects.filter(
        user=request.user
    ).values_list("followed_user", flat=True)

    """
    values_list(..., flat=True) :
    - retourne uniquement les IDs
    - flat=True transforme le résultat en liste simple
    Exemple : [3, 7, 9]
    """

    # ---------------------------------------------------
    # 2) Gestion du blocage
    # ---------------------------------------------------

    blocked_ids = UserBlock.objects.filter(
        blocker=request.user
    ).values_list("blocked_id", flat=True)

    blockers_ids = UserBlock.objects.filter(
        blocked=request.user
    ).values_list("blocker_id", flat=True)

    excluded_user_ids = list(blocked_ids) + list(blockers_ids)

    """
    excluded_user_ids :
    contient tous les utilisateurs dont on ne doit
    PAS afficher le contenu
    """

    # ---------------------------------------------------
    # 3) Tickets visibles
    # ---------------------------------------------------

    tickets = Ticket.objects.filter(
        Q(user__in=followed_users) | Q(user=request.user)
    ).exclude(
        user__in=excluded_user_ids
    )

    """
    Q() permet de faire des OR logiques.
    Ici :
    - soit le ticket appartient à un user suivi
    - soit il appartient à moi
    """

    # ---------------------------------------------------
    # 4) Reviews visibles
    # ---------------------------------------------------

    reviews = Review.objects.filter(
        Q(user__in=followed_users) |
        Q(user=request.user) |
        Q(ticket__user=request.user)  # review faite sur MES tickets
    ).exclude(
        user__in=excluded_user_ids
    )

    # ---------------------------------------------------
    # 5) Annoter pour distinguer Ticket / Review
    # ---------------------------------------------------

    tickets = tickets.annotate(
        content_type=Value("TICKET", CharField())
    )

    reviews = reviews.annotate(
        content_type=Value("REVIEW", CharField())
    )

    """
    annotate() ajoute un champ temporaire.
    content_type servira dans le template pour savoir quoi afficher.
    """

    # ---------------------------------------------------
    # 6) Fusion + tri antéchronologique
    # ---------------------------------------------------

    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )

    """
    chain() combine les deux QuerySets.
    sorted() trie par date.
    reverse=True = plus récent en premier.
    """
    # ---------------------------------------------------
    # 7) Empêcher de proposer "Créer une critique" si l'utilisateur
    #    a déjà posté une review sur ce ticket
    # ---------------------------------------------------

    reviewed_ticket_ids = set(
        Review.objects.filter(user=request.user).values_list("ticket_id", flat=True)
    )

    """
    reviewed_ticket_ids contient les IDs des tickets déjà critiqués
    par l'utilisateur connecté.

    On le passera au template pour afficher / masquer le bouton
    "Créer une critique" sur chaque ticket.
    """

    return render(request, "users/feed.html", {"posts": posts, "reviewed_ticket_ids": reviewed_ticket_ids})



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
def create_review_response_view(request, ticket_id):
    """
    Permet de créer une critique (Review) en réponse à un ticket existant.

    Règles :
    - On récupère le ticket via son id.
    - On empêche l'utilisateur de poster 2 reviews sur le même ticket.
    - En POST : on enregistre la review liée au ticket.
    - En GET : on affiche le formulaire vide.
    """

    # 1) Récupérer le ticket ou renvoyer une 404 s’il n’existe pas
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # 2) Empêcher de poster une 2ème critique sur le même ticket
    already_reviewed = Review.objects.filter(user=request.user, ticket=ticket).exists()
    if already_reviewed:
        # On renvoie vers le flux si l'utilisateur a déjà posté une critique
        return redirect("feed")

    # 3) Gestion du formulaire
    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            # commit=False = on crée l'objet sans l'enregistrer tout de suite
            review = form.save(commit=False)

            # On force le user connecté comme auteur
            review.user = request.user

            # On force le lien vers le ticket ciblé
            review.ticket = ticket

            # On peut maintenant enregistrer l'objet complet
            review.save()

            return redirect("feed")

    else:
        # GET : formulaire vide
        form = ReviewForm()

    # 4) On affiche un template dédié
    context = {
        "form": form,
        "ticket": ticket,
    }
    return render(request, "reviews/review_response.html", context)



@login_required
def update_ticket_view(request, ticket_id):
    """
    Permet de modifier un ticket existant.

    Règles :
    - Seul l'auteur du ticket peut modifier.
    - GET  : affiche le formulaire pré-rempli avec les données du ticket.
    - POST : enregistre les modifications si le formulaire est valide.
    """

    # 1) On récupère le ticket visé (ou 404 s'il n'existe pas)
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # 2) Sécurité : si l'utilisateur n'est pas l'auteur, on refuse
    if ticket.user != request.user:
        return redirect("feed")

    # 3) POST : on traite les données envoyées
    if request.method == "POST":
        # instance=ticket => Django remplit le formulaire avec l'objet existant
        # request.FILES => indispensable pour modifier l'image
        form = TicketForm(request.POST, request.FILES, instance=ticket)

        if form.is_valid():
            # form.save() met à jour le ticket existant
            form.save()
            return redirect("feed")

    else:
        # 4) GET : formulaire pré-rempli
        form = TicketForm(instance=ticket)

    return render(request, "reviews/ticket_edit.html", {"form": form, "ticket": ticket})


@login_required
def delete_ticket_view(request, ticket_id):
    """
    Permet de supprimer un ticket.

    Règles :
    - Suppression uniquement via POST (bonne pratique + cahier des charges).
    - Seul l'auteur peut supprimer.
    """

    # 1) On récupère le ticket (ou 404)
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # 2) Sécurité : seul l'auteur peut supprimer
    if ticket.user != request.user:
        return redirect("feed")

    # 3) Interdire la suppression via GET
    if request.method != "POST":
        return redirect("feed")

    # 4) Suppression en base
    ticket.delete()
    return redirect("feed")


@login_required
def update_review_view(request, review_id):
    """
    Modifie une critique existante.

    Règles :
    - Seul l'auteur de la critique peut modifier.
    - GET  : affiche le formulaire pré-rempli.
    - POST : enregistre les changements.
    """

    # 1) Récupérer la review ou 404
    review = get_object_or_404(Review, id=review_id)

    # 2) Sécurité : seul l'auteur peut modifier
    if review.user != request.user:
        return redirect("feed")

    # 3) POST : traiter le formulaire
    if request.method == "POST":
        # instance=review => pré-remplit + met à jour l'objet existant
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            return redirect("feed")

    else:
        # 4) GET : formulaire pré-rempli
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

    # 1) Récupérer la review ou 404
    review = get_object_or_404(Review, id=review_id)

    # 2) Sécurité : seul l'auteur peut supprimer
    if review.user != request.user:
        return redirect("feed")

    # 3) Interdire la suppression via GET
    if request.method != "POST":
        return redirect("feed")

    # 4) Supprimer puis retour feed
    review.delete()
    return redirect("feed")



@login_required
def follows_view(request):
    """
    Page "Abonnements" :
    - GET  : affiche la liste des utilisateurs suivis + un formulaire pour en suivre un nouveau
    - POST : traite le formulaire (ajout d'un abonnement)
    """

    # 1) Liste des abonnements actuels de l'utilisateur connecté
    # Abonnements : qui je suis
    following_relations = UserFollows.objects.filter(user=request.user).select_related("followed_user")
    
    blocked_user_ids = set(
    UserBlock.objects.filter(blocker=request.user).values_list("blocked_id", flat=True)
    )

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
                # B) Vérifier que l'utilisateur existe (ici seulement !)
                try:
                    user_to_follow = User.objects.get(username=username_to_follow)
                except User.DoesNotExist:
                    error = "Cet utilisateur n'existe pas."
                else:
                    # C) Vérifier le blocage AVANT toute création de follow
                    if is_blocked(request.user, user_to_follow):
                        error = "Impossible de suivre cet utilisateur (blocage actif)."
                    else:
                        # D) Vérifier si déjà suivi (sinon unique_together peut faire planter)
                        already_following = UserFollows.objects.filter(
                            user=request.user,
                            followed_user=user_to_follow,
                        ).exists()

                        if already_following:
                            error = "Vous suivez déjà cet utilisateur."
                        else:
                            # E) Créer l'abonnement
                            UserFollows.objects.create(
                                user=request.user,
                                followed_user=user_to_follow,
                            )
                            return redirect("follows")

    context = {
        "form": form,
        "following_relations": following_relations,
        "error": error,
        "blocked_user_ids": blocked_user_ids,  
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


@login_required
def block_view(request, user_id):
    """
    Bloque un utilisateur.
    On utilise POST pour éviter un blocage via simple clic GET.
    """
    if request.method != "POST":
        return redirect("follows")  # remplace par la page logique chez toi

    blocked = get_object_or_404(User, id=user_id)

    # Sécurité: on empêche de se bloquer soi-même (double sécurité)
    if blocked == request.user:
        return redirect("follows")

    block_user(blocker=request.user, blocked=blocked)
    return redirect("follows")


@login_required
def unblock_view(request, user_id):
    """
    Débloque un utilisateur.
    """
    if request.method != "POST":
        return redirect("follows")

    blocked = get_object_or_404(User, id=user_id)
    unblock_user(blocker=request.user, blocked=blocked)
    return redirect("follows")