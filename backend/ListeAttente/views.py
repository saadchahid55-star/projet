from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ListeAttente


@login_required
def liste_attente(request):
    #afficher la liste d'attente pour les administrateurs et les organisateurs
    if request.user.role == "administrateur":
        attentes = ListeAttente.objects.all().order_by("-id")

    elif request.user.role == "organisateur":
        attentes = ListeAttente.objects.filter(
            evenement__organisateur=request.user
        ).order_by("-id")

    else:
        messages.error(request, "Accès refusé.")
        return redirect("liste_evenements")

    return render(request, "listeAttente/liste.html", {
        "attentes": attentes
    })