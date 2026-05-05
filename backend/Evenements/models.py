

from django.db import models
from django.conf import settings
from categorie.models import Categorie




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
        on_delete=models.CASCADE,
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
    
    

    def places_restantes(self):
        return self.capacite - self.inscriptions.count()

    def est_complet(self):
        return self.places_restantes() <= 0

    def __str__(self):
        return self.titre