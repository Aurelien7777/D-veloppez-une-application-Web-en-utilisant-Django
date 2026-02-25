from django import forms
from reviews.models import Ticket, Review, UserFollows

class TicketForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ("title", "description", "image",)
        
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
        # Ajouter Bootstrap sur tous les champs du formulaire
        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'form-control'
        })
        
        # Ajouter des placeholders (optionnel mais utile pour le wireframe)
        self.fields["title"].widget.attrs["placeholder"] = "Titre"
        self.fields["description"].widget.attrs["placeholder"] = "Ecrivez votre description ici"
        #self.fields["image"].widget.attrs["type"] = "file"
        #self.fields["image"].widget.attrs["class"] = "form-control"
        
        # self.fields est un dictionnaire contenant tous les champs dont nous disposons 
        # Dans notre cas titre, description, image
        # chaque champs a une réprésentation HTML définit en fonction de son type (Charfield, PasswordField etc)
        # Widget est la réprésentation HTML de ce champs et attrs permet d'ajouter 


class ReviewForm(forms.ModelForm):
    
    """
    Formulaire pour créer une critique (Review).

    Objectif UI (wireframe) :
    - rating affiché en boutons radio de 0 à 5
    - headline et body en champs classiques
    """

    # Choix possibles pour la note (0 à 5)
    RATING_CHOICES = [(i, str(i)) for i in range(6)]

    # On surcharge le champ "rating" du modèle
    # Au lieu d'un input numérique, on veut des radios
    rating = forms.TypedChoiceField(
        label="Note",
        choices=RATING_CHOICES,
        coerce=int,  # très important : convertit "3" (str) en 3 (int)
        widget=forms.RadioSelect,
    )
    class Meta:
        model = Review
        fields = ("headline", "body", "rating")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Boucle sur tous les champs du formulaire
        # Ajouter Bootstrap sur tous les champs du formulaire 
        
        # Ajouter des placeholders (optionnel mais utile pour le wireframe)
        # Bootstrap sur les champs texte uniquement
        self.fields["headline"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Titre court",
        })
        
        self.fields["body"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Corps de la critique",
        })


class FollowForm(forms.Form):
    # L'utilisateur va taper le username exact de la personne à suivre
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=150,  # cohérent avec AbstractUser (username max_length=150)
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nom d'utilisateur à suivre",
            }
        ),
    )