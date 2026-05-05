from urllib import request

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Evenement
from .forms import EvenementForm
from Inscription.models import Inscription
from categorie.models import Categorie
from Rappel.models import Rappel
from Notification.models import Notification

def liste_evenements(request):
    evenements = Evenement.objects.all().order_by('date')

    # 🔎 filtres
    q = request.GET.get('q')
    lieu = request.GET.get('lieu')
    date = request.GET.get('date')

    if q:
        evenements = evenements.filter(titre__icontains=q)

    if lieu:
        evenements = evenements.filter(lieu__icontains=lieu)

    if date:
        evenements = evenements.filter(date=date)

    # 📊 calcul + inscription
    for evenement in evenements:
        evenement.restant = evenement.places_restantes()

    if evenement.capacite > 0:
        evenement.pourcentage = int((evenement.restant / evenement.capacite) * 100)
    else:
        evenement.pourcentage = 0

    if request.user.is_authenticated and request.user.role == "client":
        evenement.deja_inscrit = Inscription.objects.filter(
            utilisateur=request.user,
            evenement=evenement
        ).exists()
    else:
        evenement.deja_inscrit = False

    return render(request, 'evenements/liste_evenements.html', {
        'evenements': evenements
    })


def detail_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)
    return render(request, 'evenements/detail.html', {'evenement': evenement})


@login_required
def creer_evenement(request):
    if request.user.role != 'administrateur':
        messages.error(request, "Seul un administrateur peut créer un événement.")
        return redirect('liste_evenements')

    if request.method == 'POST':
        form = EvenementForm(request.POST, request.FILES)

        if form.is_valid():
            evenement = form.save(commit=False)
            evenement.organisateur = request.user
            evenement.save()
            messages.success(request, "Événement créé avec succès.")
            return redirect('liste_evenements')
    else:
        form = EvenementForm()

    return render(request, 'evenements/form.html', {'form': form})


@login_required
def modifier_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)

    if request.user.role != 'administrateur':
        messages.error(request, "Accès refusé.")
        return redirect('liste_evenements')

    if request.method == 'POST':
        form = EvenementForm(request.POST, request.FILES, instance=evenement)

        if form.is_valid():
            form.save()
            messages.success(request, "Événement modifié.")
            return redirect('detail_evenement', id=evenement.id)
    else:
        form = EvenementForm(instance=evenement)

    return render(request, 'evenements/form.html', {'form': form})


@login_required
def supprimer_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)

    if request.user.role != 'administrateur':
        messages.error(request, "Accès refusé.")
        return redirect('liste_evenements')

    if request.method == 'POST':
        evenement.delete()
        messages.success(request, "Événement supprimé.")
        return redirect('liste_evenements')

    return render(request, 'evenements/confirm_delete.html', {'evenement': evenement})


@login_required
def supprimer_categorie(request, id):
    categorie = get_object_or_404(Categorie, id=id)

    if request.user.role != "administrateur":
        messages.error(request, "Accès refusé.")
        return redirect("liste_evenements")

    categorie.delete()
    messages.success(request, "Catégorie supprimée avec succès.")

    return redirect("creer_evenement")