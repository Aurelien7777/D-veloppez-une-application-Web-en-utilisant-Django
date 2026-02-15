# On utilise les outils d'authentification fournis par Django
from django.contrib.auth import login, logout, authenticate

# On utilise le formulaire de création d'utilisateur par défaut (basé sur ton User custom)
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm

# Outils Django classiques : render = afficher un template, redirect = rediriger vers une page
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from .forms import LoginForm


@login_required
def feed(request):
    print(request.user.is_superuser)
    return render(request, "users/feed.html", )



def signup(request):
    """
    Page d'inscription :
    - Si on arrive en GET : on affiche le formulaire vide
    - Si on arrive en POST : on valide et on crée l'utilisateur
    """
    
    if request.user.is_authenticated:
        return redirect("feed")

    if request.method == "POST":
        # Création d'une instance UserCreationForm 
        # On remplit le formulaire avec ce que l'utilisateur a tapé
        # Créer une instance de notre formulaire et le remplir avec les données POST
        form = CustomUserCreationForm(request.POST)

        # Si tout est valide (mots de passe identiques, règles respectées, etc.)
        if form.is_valid():
            # On crée l'utilisateur en base (Enregistrement dans la db.sqlite)
            user = form.save()

            # On connecte automatiquement l'utilisateur juste après l'inscription
            login(request, user)

            # On redirige vers la page principale (on la créera ensuite)
            return redirect("login")
    else:
        # Si c'est un GET, on affiche un formulaire vide
        form = CustomUserCreationForm()

    return render(request, "users/signup.html", {"form": form})


def login_view(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("feed")

            return render(request, "users/login.html", {
                "form": form,
                "error": "Identifiants invalides"
            })

    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    """
    Déconnexion :
    - Supprime la session
    - Renvoie vers la page de login
    """
    logout(request)
    return redirect("login")
