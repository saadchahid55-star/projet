from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from Utilisateur.models import Utilisateur
from Evenements.models import Evenement
from Inscription.models import Inscription
from ListeAttente.models import ListeAttente
from Notification.models import Notification
from django.shortcuts import get_object_or_404, redirect
from Rappel.models import Rappel






def home(request):
    return render(request, 'base/home.html')

#vue pour la page d'accueil avec une liste des événements à venir
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
#si l'authentification est réussie, connecter l'utilisateur et le rediriger vers son dashboard en fonction de son rôle
        if user is not None:
            login(request, user)

        if user.role == "administrateur":
           return redirect("dashboard_admin")

        elif user.role == "organisateur":
           return redirect("dashboard_organisateur")

        else:
           return redirect("dashboard_participant")

    messages.error(request, "Nom utilisateur ou mot de passe incorrect.")

    return render(request, "base/login.html")

#vue pour la page d'inscription avec un formulaire d'inscription personnalisé qui inclut le choix du rôle de l'utilisateur
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data["role"]
            user.save()

            messages.success(request, "Compte créé avec succès.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "base/register.html", {"form": form})



#vue pour le dashboard de l'administrateur avec des statistiques globales et une liste des derniers événements créés
@login_required
def dashboard_admin(request):

    # sécurité
    if request.user.role != "administrateur":
        return redirect("dashboard_client")
#récupérer les statistiques globales et les derniers événements pour les afficher dans le dashboard
    context = {
        "total_users": Utilisateur.objects.count(),
        "total_events": Evenement.objects.count(),
        "total_inscriptions": Inscription.objects.count(),
        "total_attente": ListeAttente.objects.count(),
        "evenements": Evenement.objects.all().order_by("-id")[:5],
    }

    return render(request, "base/dashboard_admin.html", context)
#vue pour le dashboard du participant avec la liste de ses inscriptions, notifications et rappels
@login_required
def dashboard_participant(request):
    
    if not request.user.is_authenticated or request.user.role != "participant":
        return redirect("home")
    #récupérer les inscriptions, attentes, notifications et rappels de l'utilisateur connecté pour les afficher dans le dashboard
    inscriptions = Inscription.objects.filter(utilisateur=request.user)
    attentes = ListeAttente.objects.filter(utilisateur=request.user)
    notifications = Notification.objects.filter(utilisateur=request.user).order_by("-date_creation")
    rappels = Rappel.objects.filter(utilisateur=request.user).order_by("-id")

    context = {
        "inscriptions": inscriptions,
        "attentes": attentes,
        "notifications": notifications,
        "rappels": rappels,
    }

    return render(request, "base/dashboard_participant.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")



def desinscription(request, event_id):
    event = get_object_or_404(Evenement, id=event_id)
#vérifier si l'utilisateur est inscrit à l'événement, puis le désinscrire et gérer la liste d'attente si nécessaire
    inscription = Inscription.objects.filter(
        utilisateur=request.user,
        evenement=event
    ).first()

    if inscription:
        inscription.delete()

        
        if not event.est_complet():
            #chercher la première personne dans la liste d'attente pour cet événement
            attente = ListeAttente.objects.filter(
                evenement=event
            ).order_by('created_at').first()

            if attente:
                Inscription.objects.create(
                    utilisateur=attente.utilisateur,
                    evenement=event
                )
                attente.delete()

    return redirect('liste_evenements')



#vue pour le dashboard de l'organisateur avec la liste de ses événements, inscriptions et attentes
@login_required
def liste_attente_admin(request):
    if not request.user.is_authenticated or request.user.role != "administrateur":
       return redirect("home")

    attentes = ListeAttente.objects.all()

    return render(request, "base/liste_attente_admin.html", {
        "attentes": attentes
    })

#vue pour la gestion des catégories, accessible uniquement aux administrateurs et organisateurs
@login_required
def billets_admin(request):
    if not request.user.is_authenticated or request.user.role != "administrateur":
        return redirect("home")

    inscriptions = Inscription.objects.all()

    return render(request, "base/billets_admin.html", {
        "inscriptions": inscriptions
    })
#vue pour le dashboard de l'organisateur avec la liste de ses événements, inscriptions et attentes
@login_required
def dashboard_organisateur(request):
    if request.user.role != "organisateur":
        return redirect("home")

    evenements = Evenement.objects.filter(organisateur=request.user)
    inscriptions = Inscription.objects.filter(evenement__organisateur=request.user)
    attentes = ListeAttente.objects.filter(evenement__organisateur=request.user)

    context = {
        "total_evenements": evenements.count(),
        "total_inscriptions": inscriptions.count(),
        "total_attente": attentes.count(),
        "evenements": evenements.order_by("-id"),
        "inscriptions": inscriptions.order_by("-id"),
        "attentes": attentes.order_by("-id"),
    }

    return render(request, "base/dashboard_organisateur.html", context)
#gestion des utilisateurs, accessible uniquement aux administrateurs, avec la possibilité de bloquer, débloquer ou supprimer des comptes utilisateurs
@login_required
def gestion_utilisateurs(request):
    if request.user.role != "administrateur":
        return redirect("home")

    utilisateurs = Utilisateur.objects.exclude(id=request.user.id)

    return render(request, "base/gestion_utilisateurs.html", {
        "utilisateurs": utilisateurs
    })


@login_required
def bloquer_utilisateur(request, id):
    if request.user.role != "administrateur":
        return redirect("home")

    utilisateur = get_object_or_404(Utilisateur, id=id)

    utilisateur.is_active = False
    utilisateur.save()

    messages.success(request, "Utilisateur bloqué avec succès.")
    return redirect("gestion_utilisateurs")


@login_required
def debloquer_utilisateur(request, id):
    if request.user.role != "administrateur":
        return redirect("home")

    utilisateur = get_object_or_404(Utilisateur, id=id)

    utilisateur.is_active = True
    utilisateur.save()

    messages.success(request, "Utilisateur débloqué avec succès.")
    return redirect("gestion_utilisateurs")


@login_required
def supprimer_utilisateur(request, id):
    if request.user.role != "administrateur":
        return redirect("home")

    utilisateur = get_object_or_404(Utilisateur, id=id)

    if utilisateur.id == request.user.id:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
        return redirect("gestion_utilisateurs")

    utilisateur.delete()

    messages.success(request, "Utilisateur supprimé avec succès.")
    return redirect("gestion_utilisateurs")