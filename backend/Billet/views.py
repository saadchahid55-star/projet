from django.shortcuts import redirect, render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Billet



@login_required
def voir_billet(request, id):
    
    billet = get_object_or_404(Billet, id=id)
#rendre la page du billet uniquement si l'utilisateur connecté est le propriétaire du billet, sinon rediriger vers la page d'accueil
    if billet.inscription.utilisateur != request.user:
        return redirect('home')

    return render(request, 'billet/billet.html', {
        'billet': billet
    })