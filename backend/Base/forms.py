from django import forms
from django.contrib.auth.forms import UserCreationForm
from Utilisateur.models import Utilisateur

class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[
            ('client', 'Client'),
            ('administrateur', 'Administrateur'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Nom utilisateur"
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Email"
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Mot de passe"
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Confirmer mot de passe"
        })