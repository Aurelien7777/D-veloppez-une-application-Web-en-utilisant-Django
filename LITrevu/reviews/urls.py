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