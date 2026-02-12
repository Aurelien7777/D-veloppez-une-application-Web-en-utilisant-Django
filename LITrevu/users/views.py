# On utilise les outils d'authentification fournis par Django
from django.contrib.auth import login, logout, authenticate

# On utilise le formulaire de création d'utilisateur par défaut (basé sur ton User custom)
from django.contrib.auth.forms import UserCreationForm

# Outils Django classiques : render = afficher un template, redirect = rediriger vers une page
from django.shortcuts import render, redirect


def exemple(request):
    return render(request, "users/test.html")

def exemple2(request):
    return render(request, "users/test2.html")


def signup(request):
    """
    Page d'inscription :
    - Si on arrive en GET : on affiche le formulaire vide
    - Si on arrive en POST : on valide et on crée l'utilisateur
    """
    if request.method == "POST":
        # Création d'une instance UserCreationForm 
        # On remplit le formulaire avec ce que l'utilisateur a tapé
        # Créer une instance de notre formulaire et le remplir avec les données POST
        form = UserCreationForm(request.POST)

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
        form = UserCreationForm()

    return render(request, "users/signup.html", {"form": form})


def login_view(request):
    """
    Page de connexion :
    - On demande username + password
    - Si c'est bon : on connecte l'utilisateur
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Django vérifie si le username/password correspondent à un utilisateur
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # On connecte l'utilisateur (création de session)
            login(request, user)
            return redirect("login")  # temporaire, on redirigera vers "feed" plus tard

        # Si mauvais identifiants, on renvoie un message
        return render(request, "users/login.html", {"error": "Identifiants invalides."})

    return render(request, "users/login.html")


def logout_view(request):
    """
    Déconnexion :
    - Supprime la session
    - Renvoie vers la page de login
    """
    logout(request)
    return redirect("login")
