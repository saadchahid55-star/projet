from django import forms
from .models import Categorie

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Ex: Conférence, Atelier, Formation'
            })
        }