"""
Vues liées au suivi (follow) et au blocage (block).

Ce fichier regroupe :
- page abonnements (follow par username + liste)
- désabonnement (unfollow)
- blocage / déblocage (block/unblock)
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import FollowForm
from ..models import UserFollows, UserBlock
from ..services import block_user, unblock_user, is_blocked

User = get_user_model()


@login_required
def follows_view(request):
    """
    Page "Abonnements".

    - GET  : affiche
      * le formulaire pour suivre un user par username
      * la liste des utilisateurs suivis
      * les boutons se désabonner / bloquer / débloquer

    - POST : traite le formulaire FollowForm
    """

    # Liste des relations "je suis abonné à ..."
    following_relations = UserFollows.objects.filter(
        user=request.user
    ).select_related("followed_user")

    # Liste des IDs des utilisateurs que je bloque (utile au template)
    blocked_user_ids = set(
        UserBlock.objects.filter(blocker=request.user).values_list("blocked_id", flat=True)
    )

    form = FollowForm()
    error = None

    if request.method == "POST":
        form = FollowForm(request.POST)

        if form.is_valid():
            username_to_follow = form.cleaned_data["username"].strip()

            # Interdire de se suivre soi-même
            if username_to_follow == request.user.username:
                error = "Vous ne pouvez pas vous suivre vous-même."
            else:
                # Vérifier que l'utilisateur existe
                try:
                    user_to_follow = User.objects.get(username=username_to_follow)
                except User.DoesNotExist:
                    error = "Cet utilisateur n'existe pas."
                else:
                    # Vérifier le blocage AVANT de follow
                    if is_blocked(request.user, user_to_follow):
                        error = "Impossible de suivre cet utilisateur (blocage actif)."
                    else:
                        # Vérifier si déjà suivi
                        already_following = UserFollows.objects.filter(
                            user=request.user,
                            followed_user=user_to_follow,
                        ).exists()

                        if already_following:
                            error = "Vous suivez déjà cet utilisateur."
                        else:
                            # Créer l'abonnement
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
    Désabonnement.

    Règles :
    - Suppression via POST uniquement.
    - Seul l'utilisateur qui a créé la relation peut la supprimer.
    """

    if request.method != "POST":
        return redirect("follows")

    follow_relation = get_object_or_404(UserFollows, pk=pk)

    if follow_relation.user != request.user:
        return redirect("follows")

    follow_relation.delete()
    return redirect("follows")


@login_required
def block_view(request, user_id):
    """
    Bloque un utilisateur.

    Règles :
    - Action via POST uniquement.
    - On empêche de se bloquer soi-même.
    - La logique "métier" est dans services.py (block_user).
    """

    if request.method != "POST":
        return redirect("follows")

    blocked = get_object_or_404(User, id=user_id)

    if blocked == request.user:
        return redirect("follows")

    block_user(blocker=request.user, blocked=blocked)
    return redirect("follows")


@login_required
def unblock_view(request, user_id):
    """
    Débloque un utilisateur.

    Règles :
    - Action via POST uniquement.
    - La logique "métier" est dans services.py (unblock_user).
    """

    if request.method != "POST":
        return redirect("follows")

    blocked = get_object_or_404(User, id=user_id)
    unblock_user(blocker=request.user, blocked=blocked)
    return redirect("follows")