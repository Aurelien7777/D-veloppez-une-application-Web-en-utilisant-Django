from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Ce formulaire hérite de UserCreationForm.
    
    Cela signifie que :
    - On garde toute la logique de validation Django.
    - On peut personnaliser l'affichage (CSS, labels, etc.).
    
    On garde toute la logique Django (validation, hash du mot de passe),
    mais on peut personnaliser labels/placeholders/classes CSS.
    """
    class Meta(UserCreationForm.Meta):
        """
        Meta permet de configurer :
        - quel modèle on utilise
        - quels champs seront affichés
        """
        model = User 
        fields = ("username",) 
        # Correspond au champs que l'on veut utiliser de "UserCreationForm"
        # On affiche uniquement username
        # password1 et password2 sont automatiquement ajoutés par UserCreationForm
        
    def __init__(self, *args, **kwargs):
        """
        __init__ est appelé à chaque création du formulaire :
        - GET  : CustomUserCreationForm()
        - POST : CustomUserCreationForm(request.POST)
        
        Le constructeur permet de modifier dynamiquement les champs.
        
        Ici on ajoute la classe Bootstrap 'form-control'
        à chaque champ pour avoir un rendu propre.
        
        Autrement dit,
        on personnalise les attributs HTML des champs (widget.attrs).
        """
        super().__init__(*args, **kwargs)
        
        # Boucle sur tous les champs du formulaire
        # Ajouter Bootstrap sur tous les champs du formulaire (username + password1 + password2)
        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'form-control'
        })
        
        # Ajouter des placeholders (optionnel mais utile pour le wireframe)
        self.fields["username"].widget.attrs["placeholder"] = "Nom d'utilisateur"
        self.fields["password1"].widget.attrs["placeholder"] = "Mot de passe"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirmer le mot de passe"
        # self.fields est un dictionnaire contenant tous les champs dont nous disposons 
        # Dans notre cas username, password1, password2
        # chaque champs a une réprésentation HTML définit en fonction de son type (Charfield, PasswordField etc)
        # Widget est la réprésentation HTML de ce champs et attrs permet d'ajouter 


class LoginForm(forms.Form):
    """
    Formulaire de connexion.
    On utilise forms.Form (et non ModelForm),
    car on ne crée pas d'utilisateur ici.
    """

    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Nom d'utilisateur"
        })
    )

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Mot de passe"
        })
    )
