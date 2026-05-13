from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CategorieForm
from django.shortcuts import get_object_or_404, redirect
from .models import Categorie

def est_admin(user):
    return user.is_authenticated and user.role == "administrateur"

def est_participant(user):
    return user.is_authenticated and user.role == "participant"
def est_organisateur(user):
    return user.is_authenticated and user.role == "organisateur"



def creer_categorie(request):
    if request.user.role not in ["administrateur", "organisateur"]:
      messages.error(request, "Accès refusé.")
      return redirect("home")

    if request.method == "POST":
        form = CategorieForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie créée avec succès.")
            return redirect("creer_categorie")
    else:
        #afficher le formulaire de création de catégorie et la liste des catégories existantes
        form = CategorieForm()

    categories = Categorie.objects.all().order_by("nom")

    return render(request, "categorie/creer.html", {
        "form": form,
        "categories": categories
    })


def supprimer_categorie(request, id):
    if request.user.role not in ["administrateur", "organisateur"]:
        messages.error(request, "Accès refusé.")
        return redirect("home")

    categorie = get_object_or_404(Categorie, id=id)
    categorie.delete()
    messages.success(request, "Catégorie supprimée avec succès.")

    return redirect("creer_categorie")