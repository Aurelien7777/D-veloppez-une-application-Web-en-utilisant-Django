# On importe les réglages globaux du projet
# Cela permet notamment d'accéder au modèle User personnalisé
from django.conf import settings

# Ces validateurs servent à contrôler des valeurs numériques
# Ici : empêcher une note en dessous de 0 ou au-dessus de 5
from django.core.validators import MinValueValidator, MaxValueValidator

# Import de la base des modèles Django
# Tous les modèles doivent hériter de models.Model
from django.db import models


# -----------------------------
# MODELE : TICKET
# -----------------------------
class Ticket(models.Model):
    """
    Un Ticket représente une DEMANDE de critique.
    Exemple : "Pouvez-vous me donner votre avis sur ce livre ?"
    """

    # Titre du livre ou de l’article
    # CharField = texte court
    title = models.CharField(max_length=128)

    # Description plus détaillée de la demande
    # TextField = texte long
    # blank=True signifie : le champ est optionnel dans les formulaires
    description = models.TextField(max_length=2048, blank=True)

    # Utilisateur qui a créé le ticket
    # ForeignKey = relation entre deux tables
    # Ici : chaque ticket appartient à UN utilisateur
    # settings.AUTH_USER_MODEL = ton User personnalisé
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Image facultative (ex : couverture du livre)
    # null=True = autorisé en base de données
    # blank=True = autorisé dans les formulaires
    image = models.ImageField(null=True, blank=True)

    # Date et heure de création du ticket
    # auto_now_add=True = Django remplit ce champ automatiquement
    time_created = models.DateTimeField(auto_now_add=True)


# -----------------------------
# MODELE : REVIEW
# -----------------------------
class Review(models.Model):
    """
    Une Review représente une CRITIQUE.
    Elle peut être faite :
    - en réponse à un ticket
    - ou lors de la création directe ticket + critique
    """

    # Ticket auquel la critique est rattachée
    # Une critique est TOUJOURS liée à un ticket
    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE
    )

    # Note donnée par l'utilisateur
    # PositiveSmallIntegerField = entier positif (0, 1, 2, ...)
    # validators = contraintes sur la valeur
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),  # minimum autorisé
            MaxValueValidator(5)   # maximum autorisé
        ]
    )

    # Titre court de la critique
    headline = models.CharField(max_length=128)

    # Corps de la critique (texte principal)
    # blank=True = autorise une critique sans texte long
    body = models.TextField(max_length=8192, blank=True)

    # Utilisateur qui a écrit la critique
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Date et heure de création de la critique
    time_created = models.DateTimeField(auto_now_add=True)


# -----------------------------
# MODELE : USERFOLLOWS
# -----------------------------
class UserFollows(models.Model):
    """
    Ce modèle représente le fait qu’un utilisateur
    SUIT un autre utilisateur.
    """

    # L'utilisateur qui suit quelqu'un
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following"
    )

    # L'utilisateur qui est suivi
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by"
    )

    class Meta:
        """
        Meta permet de définir des règles supplémentaires
        sur le modèle.
        """

        # Empêche qu’un utilisateur suive deux fois la même personne
        # Exemple interdit :
        # user = Alice, followed_user = Bob (deux fois)
        unique_together = ("user", "followed_user")
