from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


# Lorsqu'une URL est entré dans la barre de navigation 
# Par exemple "http://127.0.0.1:8000/signup/"
# Django va aller chercher la vue (view) correspondant ou rattachée au path ou bout de chemin entré
urlpatterns = [
    path("ticket/", views.create_ticket_view, name="ticket_view"),
    path("review/", views.create_review_view, name="review_view"),
    path("review_ticket/", views.create_ticket_and_review_view, name="review_ticket_view"),
    path("follows/", views.follows_view, name="follows"),
    path("unfollow/<int:pk>/", views.unfollow_user_view, name="unfollow"),
    path("", views.feed, name="feed"),
    path("<int:user_id>/block/", views.block_view, name="block"),
    path("<int:user_id>/unblock/", views.unblock_view, name="unblock"),
    path("ticket/<int:ticket_id>/review/", views.create_review_response_view, name="review_response"),
    # Modifier un ticket
    path("ticket/<int:ticket_id>/edit/", views.update_ticket_view, name="ticket_edit"),
    # Supprimer un ticket (POST uniquement)
    path("ticket/<int:ticket_id>/delete/", views.delete_ticket_view, name="ticket_delete"),
    # Modifier une critique
    path("review/<int:review_id>/edit/", views.update_review_view, name="review_edit"),
    # Supprimer une critique (POST uniquement)
    path("review/<int:review_id>/delete/", views.delete_review_view, name="review_delete"),


    # "name =" permet de créer une variable réutilisable pour le path 
    # Exemple dans un gabarit HTML on va l'utiliser comme ceci:
    # <p><a href="{% url 'signup' %}">Créer un compte</a></p>
    
    #Pour créer des liens dans nos gabarits, plutôt que de répéter les chemins URL, 
    #nous donnons un name à notre modèle d'URL, 
    #puis nous utilisons la balise de gabarits {% url %} pour générer le lien.

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Désormais, les images stockées dans le répertoire MEDIA_ROOT seront servies au chemin donné parMEDIA_URL.