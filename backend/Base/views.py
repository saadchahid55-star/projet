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


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == "administrateur":
                return redirect("dashboard_admin")
            return redirect("dashboard_client")

        messages.error(request, "Nom utilisateur ou mot de passe incorrect.")

    return render(request, "base/login.html")


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




@login_required
def dashboard_admin(request):

    # sécurité
    if request.user.role != "administrateur":
        return redirect("dashboard_client")

    context = {
        "total_users": Utilisateur.objects.count(),
        "total_events": Evenement.objects.count(),
        "total_inscriptions": Inscription.objects.count(),
        "total_attente": ListeAttente.objects.count(),
        "evenements": Evenement.objects.all().order_by("-id")[:5],
    }

    return render(request, "base/dashboard_admin.html", context)

@login_required
def dashboard_client(request):
    if not request.user.is_authenticated or request.user.role != "client":
        return redirect("home")
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

    return render(request, "base/dashboard_client.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")



def desinscription(request, event_id):
    event = get_object_or_404(Evenement, id=event_id)

    inscription = Inscription.objects.filter(
        utilisateur=request.user,
        evenement=event
    ).first()

    if inscription:
        inscription.delete()

        # 🔥 Liste d’attente
        if not event.est_complet():
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




@login_required
def liste_attente_admin(request):
    if not request.user.is_authenticated or request.user.role != "administrateur":
       return redirect("home")

    attentes = ListeAttente.objects.all()

    return render(request, "base/liste_attente_admin.html", {
        "attentes": attentes
    })


@login_required
def billets_admin(request):
    if not request.user.is_authenticated or request.user.role != "administrateur":
        return redirect("home")

    inscriptions = Inscription.objects.all()

    return render(request, "base/billets_admin.html", {
        "inscriptions": inscriptions
    })