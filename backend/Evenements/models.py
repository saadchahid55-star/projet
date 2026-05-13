

from django.db import models
from django.conf import settings
from categorie.models import Categorie



# Creer votre modèle Evenement ici
class Evenement(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    lieu = models.CharField(max_length=100)
    date = models.DateField()
    heure = models.TimeField()
    duree = models.IntegerField()
    capacite = models.IntegerField()
    image = models.ImageField(upload_to='evenements/', blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True)
    organisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        #si utilisateur est supprimé, on supprime aussi les événements qu'il a créés
        on_delete=models.CASCADE,
        #acceder aux événements créés par un utilisateur 
        related_name='evenements_crees'
    )
    prix = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    devise = models.CharField(
        max_length=10,
        choices=[
        ("MAD", "MAD"),
        ("EUR", "Euro"),
        ("USD", "Dollar"),
    ],
        default="MAD"
    
    )
    
    
#place restantes = capacité - nombre d'inscriptions
    def places_restantes(self):
        return self.capacite - self.inscriptions.count()
#un événement est complet si le nombre de places restantes est inférieur ou égal à 0
    def est_complet(self):
        return self.places_restantes() <= 0
#afficher le titre de l'événement dans l'admin
    def __str__(self):
        return self.titre