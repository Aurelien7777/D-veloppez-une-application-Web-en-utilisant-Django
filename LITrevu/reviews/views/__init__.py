"""
Package des vues (dossier reviews/views/).

Ce fichier __init__.py sert de "façade" :
il expose toutes les fonctions de vues attendues par `reviews/urls.py`.

But :
- permettre `from . import views` dans urls.py
- garder un code découpé et maintenable
"""

# FEED
from .feed import feed

# TICKETS
from .tickets import (
    create_ticket_view,
    update_ticket_view,
    delete_ticket_view,
    create_ticket_and_review_view,
)

# REVIEWS
from .reviews import (
    create_review_view,
    create_review_response_view,
    update_review_view,
    delete_review_view,
)

# FOLLOWS / BLOCK
from .follows import (
    follows_view,
    unfollow_user_view,
    block_view,
    unblock_view,
)

__all__ = [
    "feed",
    "create_ticket_view",
    "update_ticket_view",
    "delete_ticket_view",
    "create_ticket_and_review_view",
    "create_review_view",
    "create_review_response_view",
    "update_review_view",
    "delete_review_view",
    "follows_view",
    "unfollow_user_view",
    "block_view",
    "unblock_view",
]
