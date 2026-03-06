# users/services.py
from django.db import transaction
from .models import UserBlock
from reviews.models import UserFollows  # adapte le chemin selon ton projet


def is_blocked(user_a, user_b) -> bool:
    """
    Retourne True si user_a bloque user_b OU user_b bloque user_a.
    (Blocage "mutuel" dans le sens des effets, pas dans la base.)
    """
    return (
        UserBlock.objects.filter(blocker=user_a, blocked=user_b).exists()
        or UserBlock.objects.filter(blocker=user_b, blocked=user_a).exists()
    )


@transaction.atomic
def block_user(blocker, blocked) -> None:
    """
    - Crée le blocage si absent
    - Supprime les follows existants dans les 2 sens pour éviter incohérences
    """
    UserBlock.objects.get_or_create(blocker=blocker, blocked=blocked)

    # Supprime toute relation de suivi entre les deux utilisateurs
    UserFollows.objects.filter(user=blocker, followed_user=blocked).delete()
    UserFollows.objects.filter(user=blocked, followed_user=blocker).delete()


def unblock_user(blocker, blocked) -> None:
    """
    Supprime la relation de blocage si elle existe.
    """
    UserBlock.objects.filter(blocker=blocker, blocked=blocked).delete()
