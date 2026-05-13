#les fcts utiles 
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
from django.db.models import Q
#vue afficher la liste des événements avec possibilité de recherche par titre, description, lieu et date
def liste_evenements(request):
    evenements = Evenement.objects.all().order_by('date')
#recuperer les paramètres de recherche
    q = request.GET.get('q')
    lieu = request.GET.get('lieu')
    date = request.GET.get('date')

    if q:
        #rechercher dans le titre et la description sans tenir compte de la casse
        evenements = evenements.filter(
            Q(titre__icontains=q) | Q(description__icontains=q)
        )

    if lieu:
        evenements = evenements.filter(lieu__icontains=lieu)

    if date:
        evenements = evenements.filter(date=date)

    for evenement in evenements:
        #appeler la méthode places_restantes pour chaque événement 
        evenement.restant = evenement.places_restantes()
        if evenement.capacite > 0:
            evenement.pourcentage = int((evenement.restant / evenement.capacite) * 100)
        else:
            evenement.pourcentage = 0
    #vérifier si l'utilisateur est connecté et s'il est client, puis vérifier s'il est déjà inscrit à l'événement
        if request.user.is_authenticated and request.user.role == "participant":
            evenement.deja_inscrit = Inscription.objects.filter(
                #utilisateur connecté et l'événement en cours
                utilisateur=request.user,
                evenement=evenement
            ).exists()
        else:
            evenement.deja_inscrit = False
    #afficher les événements dans la template
    return render(request, 'evenements/liste_evenements.html', {
        #envoie les événements à la template pour affichage
        'evenements': evenements
    })
#chercher un événement par son id et afficher les détails dans une page dédiée
def detail_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)
    #afficher les détails de l'événement dans la template
    return render(request, 'evenements/detail.html', {'evenement': evenement})


@login_required
#vue pour créer un événement, accessible uniquement aux administrateurs et organisateurs
def creer_evenement(request):
    if request.user.role not in ["administrateur", "organisateur"]:
      messages.error(request, "Seul un administrateur ou organisateur peut créer un événement.")
      return redirect("liste_evenements")
#formulaire soumis en POST, on valide les données et on crée l'événement
    if request.method == 'POST':
        form = EvenementForm(request.POST, request.FILES)
#formulaire valide, on crée l'événement en associant l'organisateur à l'utilisateur connecté, puis on redirige vers la liste des événements avec un message de succès
        if form.is_valid():
            evenement = form.save(commit=False)
            evenement.organisateur = request.user
            evenement.save()
            messages.success(request, "Événement créé avec succès.")
            return redirect('liste_evenements')
    else:
        form = EvenementForm()
#afficher le formulaire de création d'événement dans la template
    return render(request, 'evenements/form.html', {'form': form})


@login_required
#vue pour modifier un événement, accessible uniquement aux administrateurs et organisateurs (mais les organisateurs ne peuvent modifier que leurs propres événements)
def modifier_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)
#vérifier que l'utilisateur connecté est un administrateur avant de permettre la modification de l'événement
    if request.user.role not in ["administrateur", "organisateur"]:
      messages.error(request, "Accès refusé.")
      return redirect("liste_evenements")

    if request.user.role == "organisateur" and evenement.organisateur != request.user:
      messages.error(request, "Vous ne pouvez modifier que vos propres événements.")
      return redirect("liste_evenements")

    if request.method == 'POST':
        form = EvenementForm(request.POST, request.FILES, instance=evenement)
#formulaire soumis en POST, on valide les données et on modifie l'événement, puis on redirige vers la page de détails de l'événement avec un message de succès
        if form.is_valid():
            form.save()
            messages.success(request, "Événement modifié.")
            return redirect('detail_evenement', id=evenement.id)
    else:
        form = EvenementForm(instance=evenement)

    return render(request, 'evenements/form.html', {'form': form})


@login_required
#vue pour supprimer un événement, accessible uniquement aux administrateurs et organisateurs (mais les organisateurs ne peuvent supprimer que leurs propres événements)
def supprimer_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)

    if request.user.role not in ["administrateur", "organisateur"]:
      messages.error(request, "Accès refusé.")
      return redirect("liste_evenements")

    if request.user.role == "organisateur" and evenement.organisateur != request.user:
      messages.error(request, "Vous ne pouvez supprimer que vos propres événements.")
      return redirect("liste_evenements")
#confirmer la suppression de l'événement, si confirmé en POST, on supprime l'événement et on redirige vers la liste des événements avec un message de succès
    if request.method == 'POST':
        evenement.delete()
        messages.success(request, "Événement supprimé.")
        return redirect('liste_evenements')

    return render(request, 'evenements/confirm_delete.html', {'evenement': evenement})


@login_required
#vue pour supprimer une catégorie, accessible uniquement aux administrateurs
def supprimer_categorie(request, id):
    categorie = get_object_or_404(Categorie, id=id)
#
    if request.user.role not in ["administrateur", "organisateur"]:
      messages.error(request, "Seul un administrateur ou organisateur peut créer un événement.")
      return redirect("liste_evenements")

    categorie.delete()
    messages.success(request, "Catégorie supprimée avec succès.")

    return redirect("creer_evenement")