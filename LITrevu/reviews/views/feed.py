"""
Vues liées au flux (feed).

Ce fichier contient uniquement la logique du feed :
- récupérer les tickets + reviews visibles
- appliquer le blocage
- trier antéchronologiquement
"""

from itertools import chain  # combine plusieurs itérables (QuerySets)
from django.contrib.auth.decorators import login_required
from django.db.models import (
    Q,
    Value,
    CharField,
)  # Q pour OR, Value/CharField pour annotate
from django.shortcuts import render

from ..models import Ticket, Review, UserFollows, UserBlock


@login_required
def feed(request):
    """
    Affiche le flux.

    Le flux doit contenir :
    - les tickets et reviews des utilisateurs suivis
    - les tickets et reviews du user connecté
    - les reviews en réponse aux tickets du user connecté
    - le tout trié du plus récent au plus ancien
    - en excluant les contenus provenant des utilisateurs bloqués / bloqueurs
    """

    # ---------------------------------------------------
    # 1) Récupérer les utilisateurs suivis (IDs)
    # ---------------------------------------------------
    followed_users = UserFollows.objects.filter(
        user=request.user  # Correspond à l'utilisateur connecté
    ).values_list("followed_user", flat=True)

    # ---------------------------------------------------
    # 2) Gestion du blocage (IDs à exclure)
    # ---------------------------------------------------
    blocked_ids = UserBlock.objects.filter(blocker=request.user).values_list(
        "blocked_id", flat=True
    )

    blockers_ids = UserBlock.objects.filter(blocked=request.user).values_list(
        "blocker_id", flat=True
    )

    # On transforme en liste simple pour l'utiliser dans exclude()
    excluded_user_ids = list(blocked_ids) + list(blockers_ids)

    # ---------------------------------------------------
    # 3) Tickets visibles
    # ---------------------------------------------------
    tickets = Ticket.objects.filter(
        Q(user__in=followed_users) | Q(user=request.user)
    ).exclude(user__in=excluded_user_ids)

    # ---------------------------------------------------
    # 4) Reviews visibles
    # ---------------------------------------------------
    reviews = Review.objects.filter(
        Q(user__in=followed_users)  # Reviews écrites par les utilisateurs que tu suis.
        | Q(user=request.user)  # Mes propres reviews.
        | Q(ticket__user=request.user)  # reviews faites sur MES tickets
    ).exclude(user__in=excluded_user_ids)

    # ---------------------------------------------------
    # 5) Annoter pour distinguer Ticket / Review dans le template
    # ---------------------------------------------------
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    # ---------------------------------------------------
    # 6) Fusion + tri antéchronologique
    # ---------------------------------------------------
    posts = sorted(
        chain(tickets, reviews), key=lambda post: post.time_created, reverse=True
    )

    # ---------------------------------------------------
    # 7) Tickets déjà critiqués par l'utilisateur connecté
    # ---------------------------------------------------
    reviewed_ticket_ids = set(
        Review.objects.filter(user=request.user).values_list("ticket_id", flat=True)
    )

    # Review.objects.filter(user=request.user) = MES reviews (celles que j'ai écrites).
    # .values_list("ticket_id", flat=True) =
    # pour chacune de MES reviews, on récupère l’ID du ticket associé.

    # Rendu du template (ton feed est dans users/feed.html)
    return render(
        request,
        "users/feed.html",
        {
            "posts": posts,
            "reviewed_ticket_ids": reviewed_ticket_ids,
        },
    )
