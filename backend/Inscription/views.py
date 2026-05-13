from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from Evenements.models import Evenement
from .models import Inscription
from ListeAttente.models import ListeAttente
from Notification.models import Notification
from Rappel.models import Rappel
from Billet.models import Billet


@login_required
def inscrire_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)

    if request.user.role != "participant":
        messages.error(request, "Seuls les participants peuvent s’inscrire.")
        return redirect("liste_evenements")

    if Inscription.objects.filter(utilisateur=request.user, evenement=evenement).exists():
        messages.warning(request, "Vous êtes déjà inscrit à cet événement.")
        return redirect("dashboard_participant")

    if ListeAttente.objects.filter(utilisateur=request.user, evenement=evenement).exists():
        messages.warning(request, "Vous êtes déjà dans la liste d’attente.")
        return redirect("dashboard_participant")

    if evenement.places_restantes() > 0:
        Inscription.objects.create(
            utilisateur=request.user,
            evenement=evenement
        )

        Notification.objects.create(
            utilisateur=request.user,
            message=f"Votre inscription à l’événement {evenement.titre} est confirmée."
        )

        Rappel.objects.get_or_create(
            utilisateur=request.user,
            evenement=evenement,
            defaults={
        "message": f"Rappel : vous êtes inscrit à {evenement.titre}."
        }
        )
        

        messages.success(request, "Inscription confirmée.")
    else:
        #ajouter l'utilisateur à la liste d'attente si l'événement est complet
        ListeAttente.objects.create(
            utilisateur=request.user,
            evenement=evenement
        )

        Notification.objects.create(
            utilisateur=request.user,
            message=f"L’événement {evenement.titre} est complet. Vous êtes ajouté à la liste d’attente."
        )

        messages.info(request, "Événement complet. Vous êtes ajouté à la liste d’attente.")

    return redirect("dashboard_participant")


@login_required
def desinscrire_evenement(request, id):
    evenement = get_object_or_404(Evenement, id=id)

    inscription = Inscription.objects.filter(
        utilisateur=request.user,
        evenement=evenement
    ).first()

    if inscription:
        inscription.delete()

        Notification.objects.create(
            utilisateur=request.user,
            message=f"Vous êtes désinscrit de l’événement {evenement.titre}."
        )

        attente = ListeAttente.objects.filter(evenement=evenement).order_by("date_ajout").first()
#si une personne est dans la liste d'attente et qu'il y a des places disponibles, l'inscrire et la notifier
        if attente and evenement.places_restantes() > 0:
            Inscription.objects.create(
                utilisateur=attente.utilisateur,
                evenement=evenement
            )

            Notification.objects.create(
                utilisateur=attente.utilisateur,
                message=f"Bonne nouvelle ! Une place s’est libérée pour {evenement.titre}. Vous êtes maintenant inscrit."
            )

            Rappel.objects.create(
                utilisateur=attente.utilisateur,
                evenement=evenement,
                message=f"Rappel : vous êtes maintenant inscrit à {evenement.titre}."
            )

            attente.delete()

        messages.success(request, "Désinscription effectuée.")

    return redirect("dashboard_participant")






#vue pour afficher le billet d'une inscription
@login_required
def billet(request, inscription_id):
    inscription = get_object_or_404(Inscription, id=inscription_id)

    billet, created = Billet.objects.get_or_create(
        inscription=inscription,
        defaults={
            "code": f"BILLET-{inscription.id}"
        }
    )

    
    if request.user.role == "participant" and inscription.utilisateur != request.user:
        messages.error(request, "Accès refusé.")
        return redirect("liste_evenements")


    if request.user.role == "organisateur" and inscription.evenement.organisateur != request.user:
        messages.error(request, "Accès refusé.")
        return redirect("liste_evenements")

    return render(request, "inscription/billet.html", {
        "inscription": inscription,
        "billet": billet
    })

@login_required
@login_required
def liste_billets(request):
    if request.user.role == "administrateur":
        inscriptions = Inscription.objects.all().order_by("-id")

    elif request.user.role == "organisateur":
        inscriptions = Inscription.objects.filter(
            evenement__organisateur=request.user
        ).order_by("-id")

    else:
        messages.error(request, "Accès refusé.")
        return redirect("liste_evenements")

    return render(request, "inscription/liste_billets.html", {
        "inscriptions": inscriptions
    })