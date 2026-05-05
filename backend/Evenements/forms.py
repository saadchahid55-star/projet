from django import forms
from .models import Evenement


class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        # 🔥 On enlève organisateur → sera ajouté automatiquement
        fields = [
            'titre',
            'description',
            'lieu',
            'date',
            'heure',
            'duree',
            'capacite',
            'image',
            'categorie',
            'prix',
            'devise',
        ]

        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de l’événement'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Description...'
            }),

            'lieu': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lieu'
            }),

            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'heure': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),

            'duree': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Durée en minutes'
            }),

            'capacite': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de places'
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'categorie': forms.Select(attrs={
                'class': 'form-select'
            }),
            'prix': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prix'
            }),

            'devise': forms.Select(attrs={
                'class': 'form-select'
           }),
        }