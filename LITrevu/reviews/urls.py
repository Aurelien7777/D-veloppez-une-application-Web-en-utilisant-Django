from django.urls import path
from . import views


# Lorsqu'une URL est entré dans la barre de navigation 
# Par exemple "http://127.0.0.1:8000/signup/"
# Django va aller chercher la vue (view) correspondant ou rattachée au path ou bout de chemin entré
urlpatterns = [
    path("ticket/", views.ticket_view, name="ticket_view"),

    # "name =" permet de créer une variable réutilisable pour le path 
    # Exemple dans un gabarit HTML on va l'utiliser comme ceci:
    # <p><a href="{% url 'signup' %}">Créer un compte</a></p>
    
    #Pour créer des liens dans nos gabarits, plutôt que de répéter les chemins URL, 
    #nous donnons un name à notre modèle d'URL, 
    #puis nous utilisons la balise de gabarits {% url %} pour générer le lien.

]
